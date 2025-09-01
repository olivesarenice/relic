import json

import redis


class RedisConnection:
    def __init__(self, connection):
        self.conn = connection

    def read(self, table, key):
        """Reads a value from Redis using a 'table:key' pattern."""
        full_key = f"{table}:{key}"
        value = self.conn.get(full_key)
        if value:
            return json.loads(value)
        return None

    def write(self, table, key, value):
        """Writes a value to Redis using a 'table:key' pattern."""
        full_key = f"{table}:{key}"
        self.conn.set(full_key, json.dumps(value))

    def blpop(self, key, timeout=0):
        """Blocking pop from a Redis list."""
        return self.conn.blpop(key, timeout=timeout)

    def put(self, key, message):
        """Writes a message to a Redis queue (list)."""
        self.conn.rpush(key, message)


def connect(host, port, db=0):
    """Connect to Redis and return a RedisConnection object."""
    try:
        pool = redis.BlockingConnectionPool(host=host, port=port, db=db)
        r = redis.Redis(connection_pool=pool, decode_responses=True)
        r.ping()
        print(f"Successfully connected to Redis at {host}:{port}")
        return RedisConnection(r)
    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        return None
