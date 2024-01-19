import psycopg2
import psycopg2.extensions
from psycopg2 import pool
from queue import Queue
from queue import Empty

# Database configuration
INTERNAL_DB_CONNECTION = "postgres://postgres:manzisql123.@localhost/galleryWebsite"
EXTERNAL_DB_CONNECTION = "postgres://umuragearthubadmin:RkumKHLgya1cKCRa2SbA4Dq3tbIRSUSI@dpg-cmf4riacn0vc73bvjm9g-a/umuragearthubdb_6u6g"
AEXTERNAL = "postgres://umuragearthubadmin:RkumKHLgya1cKCRa2SbA4Dq3tbIRSUSI@dpg-cmf4riacn0vc73bvjm9g-a.oregon-postgres.render.com/umuragearthubdb_6u6g"
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

    # return pool.getconn()


# def close_connection(exception):
#     """Closes the database connection at the end of the request."""
#     db = g.pop("db", None)
#     if db is not None:
#         pool.putconn(db)
