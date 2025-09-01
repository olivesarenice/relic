import os
import sys
import argparse

# Add the parent directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.stores import postgres


def main():
    """Initializes the database by creating necessary tables."""
    parser = argparse.ArgumentParser(description="Initialize the PostgreSQL database.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="The host of the database to connect to.",
    )
    args = parser.parse_args()

    print(f"Connecting to the database at {args.host}...")
    conn = postgres.create_connection(args.host)
    if conn:
        print("Connection successful. Creating tables...")
        postgres.create_table(conn, postgres.CREATE_DATUM_TABLE)
        postgres.create_table(conn, postgres.CREATE_ENGRAM_TABLE)
        postgres.create_table(conn, postgres.CREATE_ERROR_TABLE)
        conn.close()
        print("Database initialization complete.")
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
