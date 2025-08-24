import json
import os
import sqlite3
from datetime import datetime

# Assuming the SQLite database is located at core/stores/data/relic.db
DATABASE_PATH = "core/stores/data/relic.db"
SAVE_REPLAY_PATH = "devtools/replays"


def generate_replay_file(ts_start: int, ts_end: int):
    """
    Reads all rows from the sqlite `datum` table within a given timestamp range
    and saves the `data_json` column into a list of JSON dicts.
    The file is saved as YYYYMMDD_HHMMSS_runtime.json.

    Args:
        ts_start (int): The start timestamp (inclusive) for filtering data.
        ts_end (int): The end timestamp (inclusive) for filtering data.
    """
    data_list = []
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Query for data_json where timestamp is between ts_start and ts_end
        cursor.execute(
            "SELECT data_json FROM datum WHERE unix_ts BETWEEN ? AND ?",
            (ts_start, ts_end),
        )
        rows = cursor.fetchall()

        for row in rows:
            try:
                # Parse the JSON string from data_json column
                json_data = json.loads(row[0])
                data_list.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from database: {e} in row: {row[0]}")
                continue

        # Generate filename with current timestamp
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{current_time}.json"

        # Save the list of JSON dicts to the file
        with open(f"{SAVE_REPLAY_PATH}/{filename}", "w") as f:
            json.dump(data_list, f, indent=4)

        print(
            f"Successfully generated replay file: {filename} with {len(data_list)} records."
        )

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Example usage:
    # You would typically call generate_replay_file with actual start and end timestamps.
    # For demonstration, using arbitrary timestamps.
    # Replace with actual timestamp values for testing.
    # For example, to get data from the last hour:
    from time import time

    end_ts = int(time())
    start_ts = end_ts - 3600  # 1 hour ago
    generate_replay_file(start_ts, end_ts)
