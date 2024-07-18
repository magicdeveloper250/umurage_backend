from . import get_db
import contextlib
from psycopg2 import sql


def get_dashboard():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT  e_id, g_id, id, c_id "
            stmt += "FROM exhibitions, paintings, painters, customers"
            query = sql.SQL(stmt)
            cursor.execute(query)

            data = cursor.fetchall()
            return data


if __name__ == "__main__":
    get_dashboard()
