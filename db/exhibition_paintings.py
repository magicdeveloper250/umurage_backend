from models.exhibitionPaintingBase import ExhibitionPaintingBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_exhibition_paintings(painting: ExhibitionPaintingBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO exhibition_painting "
            stmt += "(e_p_name, e_p_description, e_p_image, e_p_audio, e_p_owner, e_p_p_name) "
            stmt += "Values({0}, {1}, {2}, {3}, (SELECT e_id FROM exhibitions WHERE e_name ={4}), (SELECT id FROM painters WHERE username={5}))"
            query = sql.SQL(stmt).format(
                sql.Literal(painting.get_name()),
                sql.Literal(painting.get_description()),
                sql.Literal(painting.get_image()),
                sql.Literal(painting.get_audio()),
                sql.Literal(painting.get_owner()),
                sql.Literal(painting.get_painter()),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True


def get_exhibition_painting(exhibition_id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_p_id, e_p_name, e_p_description, e_p_image, e_p_audio, e_p_owner, username "
            stmt += "FROM exhibition_painting ep  LEFT JOIN painters p  ON ep.e_p_p_name= p.id "
            stmt += "where e_p_owner={0}"
            query = sql.SQL(stmt).format(sql.Literal(exhibition_id))
            cursor.execute(query)
            paintings = map(
                lambda ep: ExhibitionPaintingBase(*ep).dict(),
                cursor.fetchall(),
            )
            return list(paintings)


def get_all_exhibition_painting():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT e_p_id, e_p_name, e_p_description, e_p_image, e_p_audio, e_p_owner, username "
            stmt += "FROM exhibition_painting ep  LEFT JOIN painters p  ON ep.e_p_p_name= p.id "
            query = sql.SQL(stmt)
            cursor.execute(query)
            paintings = map(
                lambda ep: ExhibitionPaintingBase(*ep).dict(),
                cursor.fetchall(),
            )
            return list(paintings)


def delete_xhibition_painting(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "DELETE FROM exhibition_painting "
            stmt += "WHERE e_p_id={0};"
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            return True
