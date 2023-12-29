import psycopg2
import psycopg2.extensions  # For cursor optimization
from psycopg2 import pool


# Database configuration
DB_URL = "postgres://umuragearthubadmin:kkKzFp04w6rNUfNIyZbkYbyftSj9XNw4@dpg-cm78fj6d3nmc73cfmr20-a/umuragearthub_w087"
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
