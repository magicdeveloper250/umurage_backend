from models.painterbase import PainterBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_new_painter(painter: PainterBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO painters (username,phone, picture, fullname, password, email) "
            stmt += "VALUES ({0}, {1}, {2},{3},{4},{5}) "
            stmt += "RETURNING id, username, phone, picture, fullname,email,role, verified, password;"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get_username()),
                sql.Literal(painter.get_phone()),
                sql.Literal(painter.get_picture()),
                sql.Literal(painter.get_fullname()),
                sql.Literal(painter.get_password()),
                sql.Literal(painter.get_email()),
            )
            cursor.execute(query)
            added = PainterBase(*cursor.fetchone()).dict()
            cursor.execute("COMMIT")
            return added


def get_painter(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname, password,role, email "
            stmt += "FROM painters "
            stmt += "WHERE id={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            painter = cursor.fetchone()
            return painter


def verify_email(id, email):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE painters "
            stmt += "SET verified=1 "
            stmt += "WHERE id={0} AND email={1};"
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(email))
            cursor.execute(query)
            return True


def change_password(user_id, new_password):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE painters "
            stmt += "SET password={0} "
            stmt += "WHERE id={1}; "
            query = sql.SQL(stmt).format(
                sql.Literal(new_password), sql.Literal(user_id)
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True


def get_painter_by_email(email):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname, password,role, email "
            stmt += "FROM painters "
            stmt += "WHERE email={0}"
            query = sql.SQL(stmt).format(sql.Literal(email))
            cursor.execute(query)
            painter = cursor.fetchone()
            return painter


def get_painter_by_username(username):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT  id,username,phone, picture, fullname, password,role, email"
            stmt += " FROM painters "
            stmt += "WHERE username={0} and verified=1"
            query = sql.SQL(stmt).format(sql.Literal(username))
            cursor.execute(query)
            user = cursor.fetchone()
            return user


def get_painters():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname,email, role, verified "
            stmt += "FROM painters"
            cursor.execute(stmt)
            painters = map(lambda p: PainterBase(*p).dict(), cursor.fetchall())
            return list(painters)


def delete_painter(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "DELETE FROM painters "
            stmt += "WHERE id ={0} "
            stmt += "RETURNING id,username,phone, picture, fullname,email"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            deleted_painter = cursor.fetchall()
            cursor.execute("COMMIT")
            return deleted_painter


def update_painter(painter: PainterBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE painters "
            stmt += "SET username={0},phone={1}, picture={2}, fullname={3} "
            stmt += "WHERE id={4}"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get_username()),
                sql.Literal(painter.get_phone()),
                sql.Literal(painter.get_picture()),
                sql.Literal(painter.get_fullname()),
                sql.Literal(painter.get_id()),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True
