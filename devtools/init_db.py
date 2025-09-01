import os
import sys

# Add the parent directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.stores import postgres


def main():
    """Initializes the database by creating necessary tables."""
    print("Connecting to the database...")
    conn = postgres.create_connection("localhost")
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
