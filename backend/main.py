from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
import os
import boto3
import json
from dotenv import load_dotenv
from schemas import JobFormSchema, RetryJobRequest
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

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,       # Allow cookies/auth headers if needed
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)

@app.get("/jobs")
def get_jobs():
    """
    RPC endpoint to get all jobs.
    No auth or RLS check for now. Currently out of scope of this project which just focuses on the training.
    """
    response = supabase.table("jobs").select("*").execute()
    return response.data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        # forward everything from supabase to client
        # we must do it through the fastapi because the client NEVER connects to supabase directly
        await supabase_realtime_handler(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.post("/submit-job")
def submit_job(form_data: JobFormSchema):
    """
    RPC endpoint to submit a job. This works by inserting the job into Supabase AND sending it to the queue.
    """
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

@app.post("/retry-job")
def retry_job(request: RetryJobRequest):
    """
    RPC endpoint to retry a job. This works by just adding the job ID back to the queue.
    """
    job_id = request.job_id
    try:
        # Fetch the job from Supabase to make sure the job actually exists
        response = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
        if not response.data:
            return {"error": "Job not found"}

        job_data = response.data

        # Resend the job to SQS queue
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps({
                "job_id": job_id,
            })
        )
        
        return {"message": "Job successfully sent for retry", "job": job_data}
    except Exception as e:
        return {"error": str(e)}
