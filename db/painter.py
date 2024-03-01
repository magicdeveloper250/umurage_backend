from . import get_db
import contextlib
import psycopg2
from psycopg2 import sql


def add_new_painter(painter):

    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO painters (id,username,phone, picture, fullname, password, email) "
            stmt += "VALUES ({0}, {1}, {2},{3},{4},{5}, {6});"
            stmt += "INSERT INTO our_painters (id,username,phone, picture, fullname, password, email) "
            stmt += "VALUES ({7}, {8}, {9},{10},{11},{12}, {13}) "
            stmt += "RETURNING id,username,phone, picture, fullname,role, email;"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get("id")),
                sql.Literal(painter.get("username")),
                sql.Literal(painter.get("phone")),
                sql.Literal(painter.get("profilepicture")),
                sql.Literal(painter.get("fullname")),
                sql.Literal(painter.get("password")),
                sql.Literal(painter.get("email")),
                sql.Literal(painter.get("id")),
                sql.Literal(painter.get("username")),
                sql.Literal(painter.get("phone")),
                sql.Literal(painter.get("profilepicture")),
                sql.Literal(painter.get("fullname")),
                sql.Literal(painter.get("password")),
                sql.Literal(painter.get("email")),
            )
            cursor.execute(query)
            added_painter = cursor.fetchall()
            return added_painter


def get_painter(id):

    with get_db() as connection:
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
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE painters "
            stmt += "SET verified=1 "
            stmt += "WHERE id={0} AND email={1};"
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(email))
            cursor.execute(query)


def change_password(user_id, new_password):

    with get_db() as connection:
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


def get_painter_by_email(email):

    with get_db() as connection:
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
    with get_db() as connection:
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
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = (
                    "SELECT id,username,phone, picture, fullname,role, email, verified "
                )
                stmt += "FROM painters"
                cursor.execute(stmt)
                painters = cursor.fetchall()
                return painters
    except psycopg2.DatabaseError as error:
        return error


def delete_painter(id):
    with get_db() as connection:
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
