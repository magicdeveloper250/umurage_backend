from models.exhibitionBase import ExhibitionBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_new_exhibition(exhibition: ExhibitionBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO exhibitions (e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner) "
            stmt += "VALUES ({0},{1},{2},{3},{4},{5}) "
            stmt += "RETURNING e_id,e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner, e_status"
            query = sql.SQL(stmt).format(
                sql.Literal(exhibition.get_name()),
                sql.Literal(exhibition.get_start_date()),
                sql.Literal(exhibition.get_end_date()),
                sql.Literal(exhibition.get_host()),
                sql.Literal(exhibition.get_fees()),
                sql.Literal(exhibition.get_banner()),
            )
            cursor.execute(query)
            new_exhibition = ExhibitionBase(*cursor.fetchall()[0])
            cursor.execute("COMMIT")
            stmt = "INSERT INTO our_exhibitions (e_id,e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner) "
            stmt += "VALUES ({0},{1},{2},{3},{4},{5},{6}) "
            query = sql.SQL(stmt).format(
                sql.Literal(new_exhibition.get_id()),
                sql.Literal(new_exhibition.get_name()),
                sql.Literal(new_exhibition.get_start_date()),
                sql.Literal(new_exhibition.get_end_date()),
                sql.Literal(new_exhibition.get_host()),
                sql.Literal(new_exhibition.get_fees()),
                sql.Literal(new_exhibition.get_banner()),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return list(new_exhibition.dict())


def update_exhibition(exhibition: ExhibitionBase, id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE exhibitions SET e_name={0}, e_start_date={1}, e_end_date={2}, e_host={3}, e_entrace_fees={4}, e_banner={5} "
            stmt += "WHERE e_id={6}"
            query = sql.SQL(stmt).format(
                sql.Literal(exhibition.get_name()),
                sql.Literal(exhibition.get_start_date()),
                sql.Literal(exhibition.get_end_date()),
                sql.Literal(exhibition.get_host()),
                sql.Literal(exhibition.get_fees()),
                sql.Literal(exhibition.get_banner()),
                sql.Literal(id),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True


def change_exhibition_status(id, new_status):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE exhibitions SET e_status={0}"
            stmt += " WHERE e_id ={1} "
            stmt += "RETURNING e_id,e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner, e_status;"
            query = sql.SQL(stmt).format(
                sql.Literal(new_status),
                sql.Literal(id),
            )
            cursor.execute(query)
            exhibition = cursor.fetchone()
            cursor.execute("COMMIT")
            return ExhibitionBase(*exhibition).dict()


def delete_exhibition(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "DELETE FROM exhibitions "
            stmt += "WHERE e_id={0} "
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True


def get_exhibition(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner, e_status FROM exhibitions WHERE e_id={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            return list(ExhibitionBase(*cursor.fetchone()).dict())


def get_exhibitions():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner, e_status  "
            stmt += "FROM exhibitions "
            cursor.execute(stmt)
            rows = cursor.fetchall()
            result = map(lambda ex: ExhibitionBase(*ex).dict(), rows)
            return list(result)


def get_active_exhibitions():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner, e_status  "
            stmt += "FROM exhibitions "
            stmt += "WHERE e_status='active' "
            cursor.execute(stmt)
            rows = cursor.fetchall()
            result = map(lambda ex: ExhibitionBase(*ex).dict(), rows)
            return list(result)


def get_pending_exhibitions():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_name, e_start_date, e_end_date, e_banner "
            stmt += "FROM exhibitions "
            stmt += "WHERE e_status='pending' "
            cursor.execute(stmt)
            return cursor.fetchall()
