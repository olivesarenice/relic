import sqlite3
import uuid
from datetime import datetime


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


CREATE_DATUM_TABLE = """ CREATE TABLE IF NOT EXISTS datum (
                            uuid text PRIMARY KEY,
                            unix_ts integer NOT NULL,
                            iso_ts text NOT NULL,
                            collector text NOT NULL,
                            source_type text NOT NULL,
                            data_json text NOT NULL
                        ); """

CREATE_ENGRAM_TABLE = """ CREATE TABLE IF NOT EXISTS engram (
                            uuid text PRIMARY KEY,
                            unix_ts integer NOT NULL,
                            iso_ts text NOT NULL,
                            collector text NOT NULL,
                            source_type text NOT NULL,
                            data_json text NOT NULL
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
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)


def delete_table(conn, table_name):
    """Delete a table from the database
    :param conn: Connection object
    :param table_name: Name of the table to delete
    """
    try:
        sql = f"DROP TABLE IF EXISTS {table_name};"
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        print(f"Table {table_name} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting table {table_name}: {e}")


def table_exists(conn, table_name):
    """
    Check if a table exists in the database
    :param conn: Connection object
    :param table_name: Name of the table to check
    :return: True if table exists, False otherwise
    """
    try:
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        if c.fetchone() is not None:
            return True
        return False
    except sqlite3.Error as e:
        print(f"Error checking for table {table_name}: {e}")
        return False


import json


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
              VALUES(?,?,?,?,?,?) """
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
    return cur.lastrowid


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
              VALUES(?,?,?,?,?,?) """
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
    return cur.lastrowid


def insert_error(conn, error_data):
    """
    Create a new error record into the error table
    :param conn:
    :param error_data:
    :return: error id
    """
    sql = """ INSERT INTO error(id,unix_ts,iso_ts,input_data,error_message)
              VALUES(?,?,?,?,?) """
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
    return cur.lastrowid


def main():
    database = "core/stores/data/relic.db"

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # delete_table(conn, "engram")
        # delete_table(conn, "error")
        create_table(conn, CREATE_DATUM_TABLE)
        create_table(conn, CREATE_ENGRAM_TABLE)
        create_table(conn, CREATE_ERROR_TABLE)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
