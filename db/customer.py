from . import get_db
import contextlib
from psycopg2 import sql


def add_customer(customer):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO customers (c_first_name, c_last_name, c_email, c_phone, registered_for,status ) "
            stmt += "VALUES ({0},{1},{2},{3},{4},{5} )"
            query = sql.SQL(stmt).format(
                sql.Literal(customer.get("firstname")),
                sql.Literal(customer.get("lastName")),
                sql.Literal(customer.get("email")),
                sql.Literal(customer.get("phonenumber")),
                sql.Literal(customer.get("exhibition")),
                sql.Literal("pending"),
            )

            cursor.execute(query)


def get_customers(id=None):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            record = []
            if not id:
                stmt = "SELECT c_id, c_first_name, c_last_name, c_email, c_phone, registered_for,e_name, status "
                stmt += "FROM customers, exhibitions "
                stmt += "WHERE registered_for = e_id"
                query = sql.SQL(stmt)
                cursor.execute(query)
                record = cursor.fetchall()
            else:
                stmt = "SELECT c_id, c_first_name, c_last_name, c_email, c_phone, registered_for,status FROM customers WHERE c_id ={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = cursor.fetchall()
            return record


def update_customer_status(customerid, new_status):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE customers SET status={0}"
            stmt += " WHERE c_id ={1}"
            query = sql.SQL(stmt).format(
                sql.Literal(new_status),
                sql.Literal(customerid),
            )

            cursor.execute(query)
            cursor.execute("COMMIT")


def delete_customer(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "DELETE FROM customers "
            stmt += "WHERE c_id={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)


def check_payment(id, e_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT status "
            stmt += "FROM customers "
            stmt += "WHERE c_id={0} "
            stmt += "and registered_for={1}"
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(e_id))
            cursor.execute(query)
            response = cursor.fetchone()
            print(response)
            if response[0] == "active":
                return True
            return False
