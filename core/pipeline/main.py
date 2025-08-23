import argparse
import json
import os
import sys
import uuid
from datetime import datetime

# Add the parent directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import traceback

from core import config
from core.stores import redis
from core.stores.redis import connect as redis_connect
from core.stores.sqlite import create_connection, insert_engram
from core.types.base import Datum


def main():
    """Main function to listen to Redis and forward to SQLite."""
    parser = argparse.ArgumentParser(
        description="Relic Pipeline to listen to Redis and forward to SQLite."
    )
    parser.add_argument(
        "--network",
        type=str,
        help="Network configuration (e.g., 'localhost' for local Redis)",
    )
    args = parser.parse_args()

    if args.network == "localhost":
        config.REDIS_HOST = "localhost"
        print(f"Using local Redis host: {config.REDIS_HOST}")

    redis_client = redis_connect(config.REDIS_HOST, config.REDIS_PORT)
    if not redis_client:
        return

    db_path = "core/stores/data/relic.db"
    sqlite_conn = create_connection(db_path)
    if not sqlite_conn:
        print("Could not connect to SQLite.")
        return

    queue_name = "hub-inbox"
    print(f"Listening on Redis queue: {queue_name}")

    while True:
        try:
            # Blocking pop from the Redis list
            _, message_json = redis_client.blpop(queue_name)
            message = json.loads(message_json)
            print(f"Received message: {message}")

            ##################################
            # Do some engram processing here #
            print(f"Processing message <{message['uuid'][0:8]}> into an engram...")
            engram_data = message
            print("Done!")
            ##################################

            # Insert into SQLite
            if engram_data:
                insert_engram(sqlite_conn, engram_data)
                print("Inserted engram to SQLite.")
            else:
                print("No engram data to insert.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            break

    sqlite_conn.close()


if __name__ == "__main__":
    main()
