import psycopg2
import contextlib
from psycopg2 import sql
from . import get_db
import time
from auth.UserAuth import custom_login_required


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
                sql.Literal(time.asctime()),
                sql.Literal(painting.get("image")),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")


def get_paintings():
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name, username, g_category,g_created, g_image, phone, likes  "
            stmt += "FROM paintings g, painters p "
            stmt += "WHERE g.g_owner=p.id "
            cursor.execute(stmt)
            paintings = cursor.fetchall()
            return paintings


def get_painting_by_id(userId):
    custom_login_required()
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name,g_category, g_image,likes "
            stmt += "FROM paintings "
            stmt += "WHERE g_owner={0} "
            query = sql.SQL(stmt).format(sql.Literal(userId))
            cursor.execute(query)
            paintings = cursor.fetchall()
            return paintings


def delete_painting(id, owner):
    custom_login_required()
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = " BEGIN ;"
            stmt += "DELETE FROM paintings "
            stmt += "WHERE g_id={0};"

            stmt += "COMMIT "
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(owner))
            cursor.execute(query)


def like(painting_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE paintings "
            stmt += "SET likes= likes+1 "
            stmt += "WHERE g_id={0}; "
            stmt += "COMMIT;"

            query = sql.SQL(stmt).format(sql.Literal(painting_id))
            cursor.execute(query)

            return True


def dislike(painting_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE paintings "
            stmt += "SET likes= likes-1 "
            stmt += "WHERE g_id={0} ;"
            stmt += "COMMIT;"

            query = sql.SQL(stmt).format(sql.Literal(painting_id))
            cursor.execute(query)
            return True


def get_likes(painting_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT likes "
            stmt += "FROM paintings "
            stmt += "WHERE g_id={0} "

            query = sql.SQL(stmt).format(sql.Literal(painting_id))
            cursor.execute(query)
            likes = cursor.fetchone()
            return likes
