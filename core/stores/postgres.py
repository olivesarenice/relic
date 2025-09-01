import os
import psycopg2
import json
from dotenv import load_dotenv
from loguru import logger

from core import config


def create_connection(host=config.POSTGRES_HOST):
    """create a database connection to the PostgreSQL database"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            host=host,
            port=config.POSTGRES_PORT,
        )
        return conn
    except psycopg2.Error as e:
        logger.error(e)

    return conn


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


def create_table(conn, sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        logger.info("Table created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating table: {e}")
        conn.rollback()
        raise e


def insert_datum(conn, datum_data):
    """
    Create a new engram into the engram table
    :param conn:
    :param datum_data:
    :return: datum id
    """
    # Convert the JSON data to a string
    if isinstance(datum_data["data_json"], dict):
        datum_data["data_json"] = json.dumps(datum_data["data_json"])
    sql = """ INSERT INTO datum(uuid,unix_ts,iso_ts,collector,source_type,data_json)
              VALUES(%s,%s,%s,%s,%s,%s) """
    try:
        cur = conn.cursor()
        values = (
            datum_data["uuid"],
            datum_data["unix_ts"],
            datum_data["iso_ts"],
            datum_data["collector"],
            datum_data["source_type"],
            datum_data["data_json"],
        )
        cur.execute(sql, values)
        conn.commit()
    except psycopg2.Error as e:
        logger.error(f"Error inserting datum: {e}")
        conn.rollback()
        raise e


def insert_engram(conn, engram_data):
    """
    Create a new engram into the engram table
    :param conn:
    :param engram_data:
    :return: engram id
    """
    # Convert the JSON data to a string
    if isinstance(engram_data["data_json"], dict):
        engram_data["data_json"] = json.dumps(engram_data["data_json"])
    sql = """ INSERT INTO engram(uuid,unix_ts,iso_ts,collector,source_type,data_json)
              VALUES(%s,%s,%s,%s,%s,%s) """
    try:
        cur = conn.cursor()
        values = (
            engram_data["uuid"],
            engram_data["unix_ts"],
            engram_data["iso_ts"],
            engram_data["collector"],
            engram_data["source_type"],
            engram_data["data_json"],
        )
        cur.execute(sql, values)
        conn.commit()
    except psycopg2.Error as e:
        logger.error(f"Error inserting engram: {e}")
        conn.rollback()
        raise e


def insert_error(conn, error_data):
    """
    Create a new error record into the error table
    :param conn:
    :param error_data:
    :return: error id
    """
    sql = """ INSERT INTO error(id,unix_ts,iso_ts,input_data,error_message)
              VALUES(%s,%s,%s,%s,%s) """
    try:
        cur = conn.cursor()
        values = (
            error_data["id"],
            error_data["unix_ts"],
            error_data["iso_ts"],
            error_data["input_data"],
            error_data["error_message"],
        )
        cur.execute(sql, values)
        conn.commit()
    except psycopg2.Error as e:
        logger.error(f"Error inserting error: {e}")
        conn.rollback()
        raise e


def main():
    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        create_table(conn, CREATE_DATUM_TABLE)
        create_table(conn, CREATE_ENGRAM_TABLE)
        create_table(conn, CREATE_ERROR_TABLE)
        conn.close()
    else:
        logger.error("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
