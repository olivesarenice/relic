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


CREATE_ENGRAM_TABLE = """ CREATE TABLE IF NOT EXISTS engram (
                            uuid text PRIMARY KEY,
                            unix_ts integer NOT NULL,
                            iso_ts text NOT NULL,
                            collector text NOT NULL,
                            source_type text NOT NULL,
                            data_json text NOT NULL
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


import json


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


def main():
    database = "core/stores/data/relic.db"

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        delete_table(conn, "engram")
        create_table(conn, CREATE_ENGRAM_TABLE)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
