import psycopg2
import psycopg2.extensions
from psycopg2 import pool
from queue import Empty
from queue import Queue
import os

# Database configuration
INTERNAL_DB_CONNECTION = os.environ.get("INTERNAL_DB_CONNECTION")
EXTERNAL_DB_CONNECTION = os.environ.get("EXTERNAL_DB_CONNECTION")
AEXTERNAL = os.environ.get("AEXTERNAL")
INTERNAL2 = os.environ.get("INTERNAL2")
DB_URL = INTERNAL_DB_CONNECTION
MAX_CONNECTIONS = 1000

pool = pool.ThreadedConnectionPool(minconn=1, maxconn=MAX_CONNECTIONS, dsn=DB_URL)

db_pool = Queue()


def putconn(conn):
    conn = db_pool.put(conn)


def get_db():
    try:
        conn = db_pool.get(block=False)

        return conn
    except Empty as bd_queu_is_empty:
        conn = psycopg2.connect(DB_URL)
        putconn(conn)
        return db_pool.get(block=False)
