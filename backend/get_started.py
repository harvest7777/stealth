from time import time
import modal
import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Initialize SQS client
sqs = boto3.client("sqs", region_name=AWS_REGION)

app = modal.App("example-get-started")

def poll_messages():
    print("Polling for messages...")
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,  # Can set up to 10
            WaitTimeSeconds=10       # Long polling for efficiency
        )

        messages = response.get("Messages", [])
        if messages:
            for message in messages:
                body = json.loads(message["Body"])
                print("Received message:", body)

                # Delete message after processing
                print("Processing message...")
                time.sleep(30)
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                print("Message deleted from queue")
        else:
            print("No messages. Waiting...")

@app.function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2


@app.local_entrypoint()
def main():
    print("the square is", square.remote(42))

    
if __name__ == "__main__":
    poll_messages()  # Start polling for messages