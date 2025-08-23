import argparse
import os
import random
import sys
import time
from hashlib import sha256

# Add the parent directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from core import config
from core.stores import redis
from core.types.base import Datum


# --- Mock Collector ---
def mock_collector():
    """
    This is a mock collector that simulates data collection.
    It generates a Datum object with random values for testing purposes.
    """
    return Datum(
        collector="mock_collector",
        source_type="test_source",
        data_json={
            "random_string": sha256(str(random.random()).encode()).hexdigest(),
            "random_number": random.randint(1, 100),
        },
    )


# --- Authentication ---
API_KEY_NAME = "X-API-KEY"
CLIENT_ID_NAME = "X-CLIENT-ID"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
client_id_header = APIKeyHeader(name=CLIENT_ID_NAME, auto_error=False)


def is_auth(
    api_key: str = Depends(api_key_header),
    client_id: str = Depends(client_id_header),
):
    if (
        client_id in config.INGRESS_CREDENTIALS
        and api_key == config.INGRESS_CREDENTIALS[client_id]
    ):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Client ID or API Key",
        )


# --- FastAPI App ---
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",  # Allow requests from the web application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = None  # Global variable to hold the Redis connection


@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = redis.connect(config.REDIS_HOST, config.REDIS_PORT)
    print("Redis connection established.")


@app.on_event("shutdown")
async def shutdown_event():
    global redis_client
    if redis_client:
        # Assuming there's a close method or similar for the Redis client
        # If redis-py client, it might not need explicit closing for simple cases
        # but for robust applications, managing connection lifecycle is important.
        # For now, we'll just set it to None.
        redis_client = None
        print("Redis connection closed.")


# Dependency to get Redis connection
def get_redis_connection():
    global redis_client
    if not redis_client:
        # This case should ideally not happen if startup_event runs correctly
        # but as a fallback or for testing outside FastAPI context.
        redis_client = redis.connect(config.REDIS_HOST, config.REDIS_PORT)
    return redis_client


@app.get("/health")
async def health_check():
    return {"status": "ok"}


class SendRequest(BaseModel):
    collector: str
    source_type: str
    data_json: dict


def get_json_kb(data_json: dict) -> int:
    """
    Helper function to get the size of the JSON data in kbs.
    """
    return len(str(data_json).encode("utf-8")) // 1024  # Convert bytes to kilobytes


@app.post("/send")
async def send_data(
    data: SendRequest,
    is_auth: str = Depends(is_auth),
    conn=Depends(get_redis_connection),
):

    datum = Datum(
        collector=data.collector,
        source_type=data.source_type,
        data_json=data.data_json,
    )
    try:
        conn.put("hub-inbox", datum.model_dump_json())
        print(
            f"PUT -> {datum.collector}: {datum.uuid} [{get_json_kb(datum.data_json)} KB]"
        )
        return {"status": "data queued"}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send data to Redis.",
        )


# --- Main Execution ---
def run_mock_sender():
    """Runs the mock data sender loop."""
    print("Running in mock sender mode...")
    # Use a single connection for the mock sender as well
    mock_sender_conn = redis.connect()
    # Empty the queue before starting
    # Assuming mock_sender_conn.conn is the underlying redis-py client
    mock_sender_conn.conn.delete("hub-inbox")
    print("Starting to send mock data to 'hub-inbox'...")
    while True:
        data = mock_collector()
        mock_sender_conn.put("hub-inbox", data.model_dump_json())
        print(f"Sent: {data.model_dump_json()}")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Relic Proxy Server")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock sender mode instead of as a FastAPI server.",
    )
    args = parser.parse_args()

    if args.mock:
        run_mock_sender()
    else:
        import uvicorn

        print("Running FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
