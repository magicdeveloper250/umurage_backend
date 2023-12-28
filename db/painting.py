import psycopg2
import contextlib
from psycopg2 import sql
from . import get_db
from datetime import datetime


def add_new_painting(painting):
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("BEGIN")
                stmt = "INSERT INTO galleries (g_name, g_category, g_owner, g_created, g_image) "
                stmt += "VALUES ({0},{1},{2},{3},{4})"
                query = sql.SQL(stmt).format(
                    sql.Literal(painting.get("name")),
                    sql.Literal(painting.get("category")),
                    sql.Literal("4bbb5d19-4dee-40d8-a2d8-1b75da3e9d01"),
                    sql.Literal(str(datetime.now())),
                    sql.Literal(painting.get("image")),
                )
                cursor.execute(query)
                cursor.execute("COMMIT")
    except psycopg2.DatabaseError as error:
        return error


def get_paintings():
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = "SELECT g_id, g_name, p_username, g_category, g_image, p_phone  "
                stmt += "FROM paintings g, painters p "
                stmt += "WHERE g.g_owner=p.id "
                cursor.execute(stmt)
                paintings = cursor.fetchall()
                return paintings
    except psycopg2.DatabaseError as error:
        print(error)
