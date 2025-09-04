import json
import psycopg2
from functools import wraps
from loguru import logger

from core import config


def with_reconnect(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            logger.warning(f"Connection error in {func.__name__}: {e}. Reconnecting...")
            self.close()
            self.conn = self._create_connection(self.host)
            if self.conn:
                logger.info("Reconnected successfully. Retrying operation.")
                return func(self, *args, **kwargs)
            else:
                logger.error("Failed to reconnect. Operation failed.")
                raise e

    return wrapper


class PgClient:
    def __init__(self, host=config.POSTGRES_HOST):
        self.host = host
        self.conn = self._create_connection(host)
        if self.conn:
            self._initialize_tables()

    def _create_connection(self, host):
        """Create a database connection to the PostgreSQL database."""
        try:
            if config.POSTGRES_CONNECTION_STRING:
                logger.info("Using connection string for PostgreSQL connection.")
                return psycopg2.connect(config.POSTGRES_CONNECTION_STRING)
            else:
                logger.info("Using individual parameters for PostgreSQL connection.")
                return psycopg2.connect(
                    dbname=config.POSTGRES_DB,
                    user=config.POSTGRES_USER,
                    password=config.POSTGRES_PASSWORD,
                    host=host,
                    port=config.POSTGRES_PORT,
                )
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            return None

    def _initialize_tables(self):
        """Create tables if they don't exist."""
        self.create_table(self.CREATE_DATUM_TABLE)
        self.create_table(self.CREATE_ENGRAM_TABLE)
        self.create_table(self.CREATE_ERROR_TABLE)

    CREATE_DATUM_TABLE = """ CREATE TABLE IF NOT EXISTS datum (
                                uuid text PRIMARY KEY,
                                unix_ts integer NOT NULL,
                                iso_ts text NOT NULL,
                                collector text NOT NULL,
                                source_type text NOT NULL,
                                data_json jsonb NOT NULL
                            ); """

    CREATE_ENGRAM_TABLE = """ CREATE TABLE IF NOT EXISTS engram (
                                uuid text PRIMARY KEY,
                                unix_ts integer NOT NULL,
                                iso_ts text NOT NULL,
                                collector text NOT NULL,
                                source_type text NOT NULL,
                                data_json jsonb NOT NULL
                            ); """

    CREATE_ERROR_TABLE = """ CREATE TABLE IF NOT EXISTS error (
                                id text PRIMARY KEY,
                                unix_ts integer NOT NULL,
                                iso_ts text NOT NULL,
                                input_data text NOT NULL,
                                error_message text NOT NULL
                            ); """

    @with_reconnect
    def create_table(self, sql):
        """Create a table from the create_table_sql statement."""
        if not self.conn:
            logger.error("No database connection.")
            return
        try:
            with self.conn.cursor() as c:
                c.execute(sql)
            self.conn.commit()
            logger.info("Table created successfully.")
        except psycopg2.Error as e:
            logger.error(f"Error creating table: {e}")
            self.conn.rollback()
            raise e

    @with_reconnect
    def insert_datum(self, datum_data):
        """Insert a new datum record."""
        if not self.conn:
            logger.error("No database connection.")
            return
        if isinstance(datum_data.get("data_json"), dict):
            datum_data["data_json"] = json.dumps(datum_data["data_json"])
        sql = """ INSERT INTO datum(uuid,unix_ts,iso_ts,collector,source_type,data_json)
                  VALUES(%s,%s,%s,%s,%s,%s) """
        try:
            with self.conn.cursor() as cur:
                values = (
                    datum_data["uuid"],
                    datum_data["unix_ts"],
                    datum_data["iso_ts"],
                    datum_data["collector"],
                    datum_data["source_type"],
                    datum_data["data_json"],
                )
                cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error inserting datum: {e}")
            self.conn.rollback()
            raise e

    @with_reconnect
    def insert_engram(self, engram_data):
        """Insert a new engram record."""
        if not self.conn:
            logger.error("No database connection.")
            return
        if isinstance(engram_data.get("data_json"), dict):
            engram_data["data_json"] = json.dumps(engram_data["data_json"])
        sql = """ INSERT INTO engram(uuid,unix_ts,iso_ts,collector,source_type,data_json)
                  VALUES(%s,%s,%s,%s,%s,%s) """
        try:
            with self.conn.cursor() as cur:
                values = (
                    engram_data["uuid"],
                    engram_data["unix_ts"],
                    engram_data["iso_ts"],
                    engram_data["collector"],
                    engram_data["source_type"],
                    engram_data["data_json"],
                )
                cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error inserting engram: {e}")
            self.conn.rollback()
            raise e

    @with_reconnect
    def insert_error(self, error_data):
        """Insert a new error record."""
        if not self.conn:
            logger.error("No database connection.")
            return
        sql = """ INSERT INTO error(id,unix_ts,iso_ts,input_data,error_message)
                  VALUES(%s,%s,%s,%s,%s) """
        try:
            with self.conn.cursor() as cur:
                values = (
                    error_data["id"],
                    error_data["unix_ts"],
                    error_data["iso_ts"],
                    error_data["input_data"],
                    error_data["error_message"],
                )
                cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error inserting error: {e}")
            self.conn.rollback()
            raise e

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")


def main():
    pg_client = PgClient()
    if pg_client.conn:
        # The tables are already initialized in the constructor
        pg_client.close()
    else:
        logger.error("Error! Cannot create the database connection.")


if __name__ == "__main__":
    main()
