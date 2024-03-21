from models.customerBase import CustomerBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_customer(customer: CustomerBase):
    print(CustomerBase.dict(customer))
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO customers (c_first_name, c_last_name, c_email, c_phone, registered_for,status,datetime ) "
            stmt += "VALUES ({0},{1},{2},{3},{4},{5},{6} ) "
            stmt += "RETURNING c_id,c_first_name, c_last_name, c_email, c_phone, registered_for,status,datetime"
            query = sql.SQL(stmt).format(
                sql.Literal(customer.get_first_name()),
                sql.Literal(customer.get_last_name()),
                sql.Literal(customer.get_email()),
                sql.Literal(customer.get_phone()),
                sql.Literal(customer.get_register_for()),
                sql.Literal(customer.get_status()),
                sql.Literal(customer.get_datetime()),
            )
            cursor.execute(query)
            added_customer = CustomerBase(*cursor.fetchone())
            return CustomerBase.dict(added_customer)


def get_customers(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            record = None
            if not id:
                stmt = "SELECT c_id, c_first_name, c_last_name, c_email, c_phone, registered_for,e_name, status,datetime "
                stmt += "FROM customers, exhibitions "
                stmt += "WHERE registered_for = e_id"
                query = sql.SQL(stmt)
                cursor.execute(query)
                record = map(
                    lambda c: CustomerBase.dict(CustomerBase(*c)), cursor.fetchall()
                )
            else:
                stmt = "SELECT c_id, c_first_name, c_last_name, c_email, c_phone, registered_for,status,datetime FROM customers WHERE c_id ={0}"
                query = sql.SQL(stmt).format(sql.Literal(id))
                cursor.execute(query)
                record = map(
                    lambda c: CustomerBase.dict(CustomerBase(*c)), cursor.fetchall()
                )
            return list(record)


def update_customer_status(customerid, new_status, e_name):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE customers SET status={0}"
            stmt += " WHERE c_id ={1} "
            stmt += "RETURNING c_id,c_first_name, c_last_name, c_email, c_phone, registered_for,(SELECT e_name FROM exhibitions WHERE e_id={2}),status,datetime;"
            query = sql.SQL(stmt).format(
                sql.Literal(new_status),
                sql.Literal(customerid),
                sql.Literal(e_name),
            )
            cursor.execute(query)
            customer = cursor.fetchone()
            cursor.execute("COMMIT")
            return CustomerBase.dict(CustomerBase(*customer))


def delete_customer(id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM customers "
            stmt += "WHERE c_id={0};"
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            return True


def check_payment(id, e_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT status, c_id "
            stmt += "FROM customers "
            stmt += "WHERE c_id={0} "
            stmt += "and registered_for={1} and status='active'"
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(e_id))
            cursor.execute(query)
            response = cursor.fetchone()
            return response
