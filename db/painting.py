from models.paintingBase import PaintingBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_new_painting(painting: PaintingBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO paintings (g_name, g_category, g_owner, g_created, g_image) "
            stmt += "VALUES ({0},{1},{2},{3},{4}) "
            stmt += "RETURNING g_id,g_image, likes"
            query = sql.SQL(stmt).format(
                sql.Literal(painting.get_name()),
                sql.Literal(painting.get_category()),
                sql.Literal(painting.get_owner()),
                sql.Literal(painting.get_created()),
                sql.Literal(painting.get_image()),
            )
            cursor.execute(query)
            added_painting = cursor.fetchall()
            cursor.execute("COMMIT")
            return added_painting


def get_paintings():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name, username, g_category,g_created, g_image, phone, likes "
            stmt += "FROM paintings g, painters p "
            stmt += "WHERE g.g_owner=p.id "
            cursor.execute(stmt)
            paintings = cursor.fetchall()
            return paintings


def get_painting_by_id(userId):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name,g_category, g_image,likes "
            stmt += "FROM paintings "
            stmt += "WHERE g_owner={0} "
            query = sql.SQL(stmt).format(sql.Literal(userId))
            cursor.execute(query)
            paintings = cursor.fetchall()
            return paintings


def get_painting_by_painting_id(username, p_id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT g_id, g_name, username, g_category,g_created, g_image, phone, likes "
            stmt += "FROM paintings g, painters p "
            stmt += "WHERE g.g_owner=(SELECT id FROM painters WHERE username={0}) AND g.g_id={1}"
            query = sql.SQL(stmt).format(sql.Literal(username), sql.Literal(p_id))
            cursor.execute(query)
            painting = cursor.fetchall()
            return painting


def delete_painting(painting_id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM paintings "
            stmt += "WHERE g_id={0}; "
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(painting_id))
            cursor.execute(query)
            return True


def like(painting_id):
    with contextlib.closing(get_db()) as connection:
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
    with contextlib.closing(get_db()) as connection:
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
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT likes "
            stmt += "FROM paintings "
            stmt += "WHERE g_id={0} "
            query = sql.SQL(stmt).format(sql.Literal(painting_id))
            cursor.execute(query)
            likes = cursor.fetchone()
            return likes
