import psycopg2
import psycopg2.extensions  # For cursor optimization
from psycopg2 import pool

# Database configuration
INTERNAL_DB_CONNECTION = "postgres://postgres:manzisql123.@localhost/galleryWebsite"
EXTERNAL_DB_CONNECTION = "postgres://umuragearthubadmin:kUzZK1pKUMBR1Oxdpp4RMroUOfe0ApcR@dpg-cmatbmda73kc73bn55sg-a/umuragearthub_hvbo"
DB_URL = EXTERNAL_DB_CONNECTION
MAX_CONNECTIONS = 1000

pool = pool.ThreadedConnectionPool(minconn=1, maxconn=MAX_CONNECTIONS, dsn=DB_URL)


def get_db():
    """Gets a database connection from the pool within the Flask context."""
    return pool.getconn()


# def close_connection(exception):
#     """Closes the database connection at the end of the request."""
#     db = g.pop("db", None)
#     if db is not None:
#         pool.putconn(db)
