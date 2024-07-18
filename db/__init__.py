import psycopg2
import psycopg2.extensions
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.pool import PoolError
import os
import random

INTERNAL_DB_CONNECTION = os.environ.get("INTERNAL_DB_CONNECTION")
EXTERNAL_DB_CONNECTION = os.environ.get("EXTERNAL_DB_CONNECTION")
AEXTERNAL = os.environ.get("AEXTERNAL")
INTERNAL2 = os.environ.get("INTERNAL2")
# DB_URL = INTERNAL_DB_CONNECTION
DB_URL = EXTERNAL_DB_CONNECTION
MINIMUM_CONNECTIONS = 1
MAX_CONNECTIONS = 10

pool = ThreadedConnectionPool(
    minconn=MINIMUM_CONNECTIONS, maxconn=MAX_CONNECTIONS, dsn=DB_URL
)


def get_connection_key():
    return random.randint(1, MAX_CONNECTIONS)


def get_db():
    try:
        conn = pool.getconn()
        return conn
    except PoolError:
        conn = psycopg2.connect(DB_URL)
        pool.putconn(conn, get_connection_key())
        return pool.getconn()
