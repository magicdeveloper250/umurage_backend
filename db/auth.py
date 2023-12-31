from . import get_db
from psycopg2 import sql
import contextlib


def get_user(userId):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT * FROM painters "
            stmt += "WHERE id={0}"
            query = sql.SQL(stmt).format(sql.Literal(userId))
            cursor.execute(query)
            user = cursor.fetchone()
            if not user:
                return False
            elif user[0] != userId:
                return False
            elif user[0] == userId:
                return True
