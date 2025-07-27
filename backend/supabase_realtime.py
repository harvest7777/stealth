import asyncio
from dotenv import load_dotenv
import websockets
import json
import os
from typing import Optional, Dict, Any


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "jobs"


def parse_supabase_event(raw_message: str) -> Optional[Dict[str, Any]]:
    """
    Parse the raw message from Supabase and return a dictionary with action and new record.
    Only handles INSERT, UPDATE, DELETE events.
    """
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

async def send_heartbeat(ws):
    """
    Send a heartbeat message every 30 seconds to keep the WebSocket connection alive.
    """
    while True:
        await asyncio.sleep(30)
        await ws.send(json.dumps({
            "topic": "phoenix",
            "event": "heartbeat",
            "payload": {},
            "ref": "2"
        }))

async def supabase_realtime_handler(fastapi_ws):
    """
    Handle real-time updates from Supabase and forward them to the FastAPI WebSocket.
    """

    realtime_url = os.getenv("SUPABASE_URL").replace("https://", "wss://") + "/realtime/v1/websocket?apikey=" + os.getenv("SUPABASE_KEY")
    async with websockets.connect(realtime_url) as ws:
        # Subscribe to table
        await ws.send(json.dumps({
            "topic": "realtime:public:jobs",
            "event": "phx_join",
            "payload": {},
            "ref": "1"
        }))

        # Start heartbeat task to keep connection alive
        asyncio.create_task(send_heartbeat(ws))

        # Receive messages from supabase and forward to client through fastapi
        async for message in ws:
            parsed_event = parse_supabase_event(message)
            if parsed_event:
                await fastapi_ws.send_text(json.dumps(parsed_event))

