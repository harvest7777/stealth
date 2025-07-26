import threading
import time
from dotenv import load_dotenv
import requests
import websocket
import json
import os
from typing import Optional, Dict, Any


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "jobs"
def test_hello():
    """
    Test the /hello POST endpoint.
    """
    url = "http://localhost:8000/hello"

    response = requests.post(url)

    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

def test_submit_job():
    """
    Test the /submit-job endpoint.
    """
    url = "http://localhost:8000/submit-job"

    response = requests.post(url)

    print("Status code:", response.status_code)
    # print("Response JSON:", response.json())

def send_heartbeat(ws):
    while True:
        time.sleep(30)
        ws.send(json.dumps({
            "topic": "phoenix",
            "event": "heartbeat",
            "payload": {},
            "ref": "2"
        }))
        print("Sent heartbeat")

def parse_supabase_event(raw_message: str) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(raw_message)

        event = data.get("event")
        payload = data.get("payload", {})

        # Only handle INSERT, UPDATE, DELETE
        if event not in ["INSERT", "UPDATE", "DELETE"]:
            return None

        return {
            "action": event,
            "new_record": payload.get("record"),
        }
    except json.JSONDecodeError:
        return None

def test_realtime():
    realtime_url = SUPABASE_URL.replace("https://", "wss://") + "/realtime/v1/websocket?apikey=" + SUPABASE_KEY
    ws = websocket.WebSocket()
    ws.connect(realtime_url)

    # Subscribe to table changes
    join_payload = {
        "topic": f"realtime:public:{TABLE}",
        "event": "phx_join",
        "payload": {},
        "ref": "1"
    }
    ws.send(json.dumps(join_payload))
    print(f"Subscribed to Supabase Realtime for {TABLE}")

    # Start heartbeat in background
    threading.Thread(target=send_heartbeat, args=(ws,), daemon=True).start()

    while True:
        message = ws.recv()
        print(parse_supabase_event(message))

if __name__ == "__main__":
    test_realtime()