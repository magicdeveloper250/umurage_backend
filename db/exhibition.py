import psycopg2
import queue
import contextlib
from psycopg2 import sql
from . import get_db


def add_new_exhibition(exhibition):
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("BEGIN")
                stmt = "INSERT INTO exhibitions (e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner) "
                stmt += "VALUES ({0},{1},{2},{3},{4},{5})"
                query = sql.SQL(stmt).format(
                    sql.Literal(exhibition["name"]),
                    sql.Literal(exhibition["start_date"]),
                    sql.Literal(exhibition["end_date"]),
                    sql.Literal(exhibition["host"]),
                    sql.Literal(exhibition["entrace_fees"]),
                    sql.Literal(exhibition["banner"]),
                )

                cursor.execute(query)
                cursor.execute("COMMIT")

    except psycopg2.DatabaseError as error:
        print(error)


def get_exhibition(id):
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = "SELECT e_id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner FROM exhibitions WHERE e_id={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = cursor.fetchall()
                return record
    except psycopg2.DatabaseError as error:
        print(error)


def get_exhibitions():
    try:
        with get_db() as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute("SET search_path TO public")
                stmt = "SELECT e_id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner  "
                stmt += "FROM exhibitions "
                cursor.execute(stmt)
                paintings = cursor.fetchall()
                return paintings
    except psycopg2.DatabaseError as error:
        print(error)
