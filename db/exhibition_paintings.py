from models.exhibitionPaintingBase import ExhibitionPaintingBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_exhibition_paintings(painting: ExhibitionPaintingBase):
    with get_db() as connection:
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
            return True


def get_exhibition_painting(exhibition_id):
    with get_db() as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT * "
            stmt += "FROM exhibition_painting "
            stmt += "where e_p_owner={0}"
            query = sql.SQL(stmt).format(sql.Literal(exhibition_id))
            cursor.execute(query)
            paintings = map(
                lambda ep: ExhibitionPaintingBase.dict(ExhibitionPaintingBase(*ep)),
                cursor.fetchall(),
            )
            return list(paintings)
