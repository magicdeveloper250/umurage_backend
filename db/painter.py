import psycopg2
import contextlib
from psycopg2 import sql
from flask import current_app
from . import get_db


def add_new_painter(painter):
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("BEGIN")
                stmt = (
                    "INSERT INTO painters (id,username,email,phone, picture, password) "
                )
                stmt += "VALUES ({0}, {1}, {2},{3},{4},{5})"
                query = sql.SQL(stmt).format(
                    sql.Literal(painter.get("id")),
                    sql.Literal(painter.get("username")),
                    sql.Literal(painter.get("email")),
                    sql.Literal(painter.get("phonenumber")),
                    sql.Literal(painter.get("profilepicture")),
                    sql.Literal(painter.get("password")),
                )
                cursor.execute(query)
                cursor.execute("COMMIT")
    except Exception as error:
        print(error)


def get_painter(id):
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = "SELECT id,username,email, picture "
                stmt += "FROM painters "
                stmt += "WHERE id={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                painter = cursor.fetchone()
                return painter
    except psycopg2.DatabaseError as error:
        return error


def get_painter_by_username(username):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT  id, username,email,phone, picture, password,role "
            stmt += " FROM painters "
            stmt += "WHERE username={0}"
            query = sql.SQL(stmt).format(sql.Literal(username))
            cursor.execute(query)
            user = cursor.fetchone()
            return user


def get_painters():
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = "SELECT id,username, email, phone, picture "
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
            stmt += "WHERE id ={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            cursor.execute("COMMIT")
