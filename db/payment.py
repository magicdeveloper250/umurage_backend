from . import get_db
from psycopg2 import sql
import contextlib
import time


def add_payment(payment_info):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO payments "
            stmt += "(pay_for, pay_customer, pay_value, pay_time, pay_via, pay_phone_number) "
            stmt += "VALUES ({0},{1},{2}, {3},{4},{5}) "
            query = sql.SQL(stmt).format(
                sql.Literal(payment_info["pay_for"]),
                sql.Literal(payment_info["pay_customer"]),
                sql.Literal(payment_info["pay_value"]),
                sql.Literal(time.asctime()),
                sql.Literal(payment_info["pay_via"]),
                sql.Literal(payment_info["pay_phone_number"]),
            )
            cursor.execute(query)


def get_payments():
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT * FROM payments "
            query = sql.SQL(stmt)
            cursor.execute(query)


def delete_payments(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN "
            stmt += "DELETE FROM payments "
            stmt += "WHERE pay_id ={0} "
            stmt += "COMMIT"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
