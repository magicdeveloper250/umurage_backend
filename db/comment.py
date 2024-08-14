from models.commentBase import CommentBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_comment(comment: CommentBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO comments (exid, custid, text) "
            stmt += "VALUES ({0},{1},{2} ) "
            stmt += "RETURNING id, exid, custid, text"
            query = sql.SQL(stmt).format(
                sql.Literal(comment.get_ex_id()),
                sql.Literal(comment.get_cust_id()),
                sql.Literal(comment.get_text()),
            )
            cursor.execute(query)
            blogs = map(lambda c: CommentBase(*c).dict(), cursor.fetchall())
            cursor.execute("COMMIT")
            return list(blogs)


def get_comments(id=None):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            record = None
            if id:
                stmt = "SELECT id, exid, custid, text "
                stmt += "FROM comments "
                stmt += "WHERE id ={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = map(lambda c: CommentBase(*c).dict(), cursor.fetchall())
            else:
                stmt = "SELECT * "
                stmt += "FROM blogs "
                query = sql.SQL(stmt)
                cursor.execute(query)
                record = map(lambda c: CommentBase(*c).dict(), cursor.fetchall())
            return list(record)


def delete_comment(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM comments "
            stmt += "WHERE id={0} "
            stmt += "RETURNING id, exid, custid, text;"
            stmt += "COMMIT"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            return True
