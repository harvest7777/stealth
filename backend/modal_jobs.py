import modal
from time import sleep
import os

# Create an image with supabase to update job status
image = modal.Image.debian_slim().pip_install("supabase")
app = modal.App("example-get-started")


@app.function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2

@app.function(image=image,
              secrets=[modal.Secret.from_name("custom-secret")]
)
def supabase_function():
    """
    This is just a dummy function to demonstrate training some job, taking 20s total.
    """
    from supabase import create_client
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    job_id = "6a5223d2-4d44-4b4b-be54-ba86bbbbdd72"

    supabase.table("jobs").update({"status": "pending"}).eq("id", job_id).execute()
    print(f"Dummy function processing")
    sleep(5)
    supabase.table("jobs").update({"status": "training"}).eq("id", job_id).execute()
    sleep(15)
    supabase.table("jobs").update({"status": "completed"}).eq("id", job_id).execute()

@app.local_entrypoint()
def main():
    print("the square is", square.remote(42))
    