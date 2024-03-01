from . import get_db
import contextlib
from psycopg2 import sql


def add_blog(blog: dict):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO blogs (b_title, b_content, b_created, b_author) "
            stmt += "VALUES ({0},{1},{2},{3} ) "
            stmt += "RETURNING b_id, b_title, b_content, b_created, b_author"
            query = sql.SQL(stmt).format(
                sql.Literal(blog.get("title")),
                sql.Literal(blog.get("content")),
                sql.Literal(blog.get("created")),
                sql.Literal(blog.get("author")),
            )

            cursor.execute(query)
            return cursor.fetchall()


def get_blogs(id=None):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            record = []
            if id:
                stmt = "SELECT b_id, b_title, b_content, b_created, b_author "
                stmt += "FROM blogs "
                stmt += "WHERE b_id ={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = cursor.fetchall()
            else:
                stmt = "SELECT * "
                stmt += "FROM blogs "
                query = sql.SQL(stmt)
                cursor.execute(query)
                record = cursor.fetchall()
            return record


def delete_blog(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM blogs "
            stmt += "WHERE b_id={0} "
            stmt += "RETURNING b_id, b_title, b_content, b_created, b_author"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            deleted_blog = cursor.fetchall()
            cursor.execute("COMMIT")
            return deleted_blog
