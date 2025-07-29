import os 
from dotenv import load_dotenv
from supabase import create_client
import json
import boto3
import modal
import time

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize AWS SQS client
sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION
)


def poll_sqs():
    """
    Continuously poll the SQS queue for new messages and process them.
    """
    print("✅ SQS Polling started...")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10  # Long polling for efficiency
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

                    
                    print("📋 Job details:", job)
                    job_dataset_repo_id = job.get("dataset_repo_id")
                    job_model_id = job.get("model_id")
                    job_policy_name = job.get("policy_name")
                    job_save_freq = job.get("save_freq", 100000)
                    job_log_freq = job.get("log_freq", 5)
                    job_gpu_type = job.get("gpu_type", "A100")

                    # Submit the job to Modal
                    # time.sleep(25)

                    gpu_to_function_name = {
                        "A100": "run_lerobot_a100",
                        "H100": "run_lerobot_h100",
                    }
                    function_name = gpu_to_function_name.get(job_gpu_type, "run_lerobot_a100")
                    f = modal.Function.from_name("lerobot-finetune-app", function_name)

                    try:
                        upload_repo = f.remote(
                            dataset_repo_id=job_dataset_repo_id,
                            model_id=job_model_id,
                            policy_name=job_policy_name,
                            save_freq=job_save_freq,
                            log_freq=job_log_freq,
                            steps=20
                        )
                        # Update job status to 'completed' in Supabase
                        try:
                            supabase.table("jobs").update({"status": "completed"}).eq("id", job_id).execute()
                            supabase.table("jobs").update({"upload_repo": upload_repo}).eq("id", job_id).execute()
                        except Exception as e:
                            print(f"❌ Error updating job status and upload repo to for {job_id}: {e}")
                    except Exception as e:
                        supabase.table("jobs").update({"status": "failed"}).eq("id", job_id).execute()
                        print(f"❌ Error submitting job to Modal: {e}")
                        continue

                    print("✅ Job offhanded to Modal.")


                    # Delete message after processing
                    sqs.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    print("✅ Message processed and deleted.")
                    time.sleep(1)
            else:
                print("No messages...")
        except Exception as e:
            print("❌ Polling error:", e)

if __name__ == "__main__":
    poll_sqs()