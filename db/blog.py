from models.blogBase import BlogBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_blog(blog: BlogBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO blogs (b_title, b_content, b_created, b_author) "
            stmt += "VALUES ({0},{1},{2},{3} ) "
            stmt += "RETURNING b_id, b_title, b_content, b_created, b_author"
            query = sql.SQL(stmt).format(
                sql.Literal(blog.get_title()),
                sql.Literal(blog.get_content()),
                sql.Literal(blog.get_created()),
                sql.Literal(blog.get_author()),
            )
            cursor.execute(query)
            blogs = map(lambda b: BlogBase(*b).dict(), cursor.fetchall())
            cursor.execute("COMMIT")
            return list(blogs)


def get_blogs(id=None):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            record = None
            if id:
                stmt = "SELECT b_id, b_title, b_content, b_created, b_author "
                stmt += "FROM blogs "
                stmt += "WHERE b_id ={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = map(lambda b: BlogBase(*b).dict(), cursor.fetchall())
            else:
                stmt = "SELECT * "
                stmt += "FROM blogs "
                query = sql.SQL(stmt)
                cursor.execute(query)
                record = map(lambda b: BlogBase(*b).dict(), cursor.fetchall())
            return list(record)


def delete_blog(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM blogs "
            stmt += "WHERE b_id={0} "
            stmt += "RETURNING b_id, b_title, b_content, b_created, b_author;"
            stmt += "COMMIT"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            return True
