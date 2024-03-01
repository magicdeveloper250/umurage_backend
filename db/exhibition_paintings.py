from . import get_db
from psycopg2 import sql
import contextlib


def add_exhibition_paintings(painting_information):
    print(painting_information["owner"])
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO exhibition_painting "
            stmt += "(e_p_name, e_p_description, e_p_image, e_p_audio, e_p_owner, e_p_p_name) "
            stmt += "Values({0}, {1}, {2}, {3}, (SELECT e_id FROM exhibitions WHERE e_name ={4}), (SELECT id FROM painters WHERE username={5}))"
            query = sql.SQL(stmt).format(
                sql.Literal(painting_information["name"]),
                sql.Literal(painting_information["description"]),
                sql.Literal(painting_information["image"]),
                sql.Literal(painting_information["audio"]),
                sql.Literal(painting_information["owner"]),
                sql.Literal(painting_information["painter"]),
            )
            cursor.execute(query)


def get_exhibition_painting(exhibition_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT * "
            stmt += "FROM exhibition_painting "
            stmt += "where e_p_owner={0}"
            query = sql.SQL(stmt).format(sql.Literal(exhibition_id))
            cursor.execute(query)
            paintings = cursor.fetchall()
            return paintings
