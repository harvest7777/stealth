import asyncio
import os
import json
from dotenv import load_dotenv
from supabase import create_client
import boto3
import modal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
sqs = boto3.client("sqs", region_name=AWS_REGION)


async def process_job(job_id, job_dataset_repo_id, job_model_id, job_policy_name, job_save_freq, job_log_freq):
    """
    Asynchronously process a job by invoking the Modal function to run the training.
    We choose asynchronous here to allow multiple models to train concurrently
    """
    gpu_to_function_name = {
        "A100": "run_lerobot_a100",
        "H100": "run_lerobot_h100",
    }
    function_name = gpu_to_function_name.get("A100", "run_lerobot_a100")
    f = modal.Function.from_name("lerobot-finetune-app", function_name)

    try:
        upload_repo = await f.remote.aio(
            dataset_repo_id=job_dataset_repo_id,
            model_id=job_model_id,
            policy_name=job_policy_name,
            save_freq=job_save_freq,
            log_freq=job_log_freq,
            steps=20
        )
        await asyncio.to_thread(supabase.table("jobs").update({"status": "completed"}).eq("id", job_id).execute)
        await asyncio.to_thread(supabase.table("jobs").update({"upload_repo": upload_repo}).eq("id", job_id).execute)
        print(f"✅ Job {job_id} completed and repo updated.")
    except Exception as e:
        print(f"❌ Error submitting job or updating Supabase for {job_id}: {e}")
        await asyncio.to_thread(supabase.table("jobs").update({"status": "failed"}).eq("id", job_id).execute)


async def poll_sqs():
    """
    Continuously poll the SQS queue for new messages and process them.
    *** THE ACTUAL TRAINING IS ASYNCHRONOUS ***
    """
    print("✅ SQS Polling started...")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            )
            messages = response.get("Messages", [])

            if messages:
                for message in messages:
                    body = json.loads(message["Body"])
                    print("📩 Received message:", body)
                    job_id = body.get("job_id")

                    job = None
                    try:
                        job = supabase.table("jobs").select("*").eq("id", job_id).single().execute().data
                    except Exception as e:
                        print(f"❌ Error fetching job from Supabase {job_id}: {e}")
                        continue

                    try:
                        supabase.table("jobs").update({"status": "training"}).eq("id", job_id).execute()
                    except Exception as e:
                        print(f"❌ Error updating job status to 'training' for {job_id}: {e}")
                        continue

                    job_dataset_repo_id = job.get("dataset_repo_id")
                    job_model_id = job.get("model_id")
                    job_policy_name = job.get("policy_name")
                    job_save_freq = job.get("save_freq", 100000)
                    job_log_freq = job.get("log_freq", 5)

                    # Fire and forget (no await)
                    asyncio.create_task(
                        process_job(job_id, job_dataset_repo_id, job_model_id, job_policy_name, job_save_freq, job_log_freq)
                    )

                    sqs.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    print("✅ Message processed and deleted.")
                    await asyncio.sleep(1)  # use asyncio.sleep here
            else:
                print("No messages...")
                await asyncio.sleep(1)
        except Exception as e:
            print("❌ Polling error:", e)
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(poll_sqs())
