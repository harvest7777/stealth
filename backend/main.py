import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from contextlib import asynccontextmanager
import os
import boto3
import json
from dotenv import load_dotenv

from utils import JobFormSchema
from supabase_realtime import supabase_realtime_handler

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(dummy_poll_sqs())
    yield

app = FastAPI(lifespan=lifespan)

async def dummy_poll_sqs():
    """
    Continuously poll the SQS queue for new messages and process them.
    This is just a dummy so we will use sleep instead of calling modal.
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

                    # NOTE: no need to await here, supabase's python client is blocking synchronous
                    supabase.table("jobs").update({"status": "training"}).eq("id", job_id).execute()
                    await asyncio.sleep(8)  # Simulate processing
                    supabase.table("jobs").update({"status": "completed"}).eq("id", job_id).execute()

                    # Delete message after processing
                    sqs.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    print("✅ Message processed and deleted.")
            else:
                print("No messages...")
        except Exception as e:
            print("❌ Polling error:", e)
# this is only because I'm trying to prototype

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,       # Allow cookies/auth headers if needed
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)

@app.get("/jobs")
def get_jobs():
    response = supabase.table("jobs").select("*").execute()
    return response.data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # forward everything from supabase to client
    # we must do it through the fastapi because the client NEVER connects to supabase directly
    await supabase_realtime_handler(websocket)


@app.post("/submit-job")
def submit_job(form_data: JobFormSchema):
    # insert job + send queue
    # return confirmation
    data = form_data.model_dump()
    try:
        response = supabase.table("jobs").insert(data).execute()
        # if it successfully isnerted into supabase, we can now send it to the queue
        inserted_job = response.data[0]
        job_id = inserted_job["id"]
        # Send job to SQS queue
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps({
                "job_id": job_id,
            })
        )
        return {"job": inserted_job, "message": "Job submitted successfully"}
    except Exception as e:
        return {"error": str(e)}

