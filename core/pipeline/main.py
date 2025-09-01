import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from loguru import logger

# Add the parent directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import traceback

from core import config
from core.stores import redis
from core.stores.redis import connect as redis_connect
from core.stores.postgres import (
    create_connection,
    insert_engram,
    insert_error,
    insert_datum,
)
from core.types.base import Datum


def main():
    """Main function to listen to Redis and forward to Postgres."""
    parser = argparse.ArgumentParser(
        description="Relic Pipeline to listen to Redis and forward to Postgres."
    )
    parser.add_argument(
        "--network",
        type=str,
        help="Network configuration (e.g., 'localhost' for local Redis)",
    )
    args = parser.parse_args()

    if args.network == "localhost":
        config.REDIS_HOST = "localhost"
        logger.info(f"Using local Redis host: {config.REDIS_HOST}")

    redis_client = redis_connect(config.REDIS_HOST, config.REDIS_PORT)
    if not redis_client:
        return

    postgres_conn = create_connection()
    if not postgres_conn:
        logger.error("Could not connect to Postgres.")
        return

    queue_name = "hub-inbox"
    logger.info(f"Listening on Redis queue: {queue_name}")

    while True:
        message_json = None
        try:
            # Blocking pop from the Redis list
            _, d = redis_client.blpop(queue_name)
            datum_json = json.loads(d)
            logger.info(f"Received message: {datum_json}")
            insert_datum(postgres_conn, datum_json)
            logger.info(f"datum logged to db")

            ##################################
            # Do some engram processing here #
            logger.info(
                f"Processing message <{datum_json['uuid'][0:8]}> into an engram..."
            )
            engram_data = datum_json
            engram_data["data_json"] = {"some_new_key": "some_processed_values"}
            logger.info("Done!")
            ##################################

            # Insert into Postgres
            if engram_data:
                insert_engram(postgres_conn, engram_data)
                logger.info("Inserted engram to Postgres.")
            else:
                logger.warning("No engram data to insert.")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            if message_json:
                now = datetime.now(timezone.utc)
                error_data = {
                    "id": str(uuid.uuid4()),
                    "unix_ts": int(now.timestamp()),
                    "iso_ts": now.isoformat(),
                    "input_data": message_json,
                    "error_message": f"{e}\n{traceback.format_exc()}",
                }
                insert_error(postgres_conn, error_data)
                logger.info("Error logged to Postgres.")

    postgres_conn.close()


if __name__ == "__main__":
    main()
