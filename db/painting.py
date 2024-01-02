import psycopg2
import contextlib
from psycopg2 import sql
from . import get_db
from datetime import datetime


def add_new_painting(painting):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "INSERT INTO paintings (g_name, g_category, g_owner, g_created, g_image) "
            stmt += "VALUES ({0},{1},{2},{3},{4})"
            query = sql.SQL(stmt).format(
                sql.Literal(painting.get("name")),
                sql.Literal(painting.get("category")),
                sql.Literal(painting.get("owner")),
                sql.Literal(str(datetime.now())),
                sql.Literal(painting.get("image")),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")


def get_paintings():
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name, username, g_category, g_image, phone  "
            stmt += "FROM paintings g, painters p "
            stmt += "WHERE g.g_owner=p.id "
            cursor.execute(stmt)
            paintings = cursor.fetchall()
            return paintings


def get_painting_by_id(userId):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name,g_category, g_image "
            stmt += "FROM paintings "
            stmt += "WHERE g_owner={0} "
            query = sql.SQL(stmt).format(sql.Literal(userId))
            cursor.execute(query)
            paintings = cursor.fetchall()
            return paintings


def delete_painting(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "DELETE FROM paintings "
            stmt += "WHERE g_id={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
