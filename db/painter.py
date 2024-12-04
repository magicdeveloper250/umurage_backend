from models.painterbase import PainterBase
from psycopg2 import sql
from . import get_db
import contextlib


def add_new_painter(painter: PainterBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "INSERT INTO painters (username,phone, picture, fullname, password, email, bio) "
            stmt += "VALUES ({0}, {1}, {2},{3},{4},{5}, {6}) "
            stmt += "RETURNING id, username, phone, picture, fullname,email,role, verified, password;"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get_username()),
                sql.Literal(painter.get_phone()),
                sql.Literal(painter.get_picture()),
                sql.Literal(painter.get_fullname()),
                sql.Literal(painter.get_password()),
                sql.Literal(painter.get_email()),
                sql.Literal(painter.get_bio()),
            )
            cursor.execute(query)
            added = PainterBase(*cursor.fetchone()).dict()
            cursor.execute("COMMIT")
            stmt = "INSERT INTO social_medias (p_id,instagram, facebook, x, youtube, tiktok) "
            stmt += "VALUES ({0}, {1}, {2},{3},{4},{5}) "
            print(painter.dict())
            query = sql.SQL(stmt).format(
                sql.Literal(str(added.get("id"))),
                sql.Literal(None),
                sql.Literal(None),
                sql.Literal(None),
                sql.Literal(None),
                sql.Literal(None),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return added


def get_painter(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname, password,role, email "
            stmt += "FROM painters "
            stmt += "WHERE id={0}"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            painter = cursor.fetchone()
            return painter


def verify_email(id, email):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "BEGIN;"
            stmt += "UPDATE painters "
            stmt += "SET verified=1 "
            stmt += "WHERE id={0} AND email={1};"
            stmt += "COMMIT;"
            query = sql.SQL(stmt).format(sql.Literal(id), sql.Literal(email))
            cursor.execute(query)
            return True


def change_password(user_id, new_password):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE painters "
            stmt += "SET password={0} "
            stmt += "WHERE id={1}; "
            query = sql.SQL(stmt).format(
                sql.Literal(new_password), sql.Literal(user_id)
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True


def get_painter_by_email(email):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname, password,role, email "
            stmt += "FROM painters "
            stmt += "WHERE email={0}"
            query = sql.SQL(stmt).format(sql.Literal(email))
            cursor.execute(query)
            painter = cursor.fetchone()
            return painter


def get_painter_by_username(username):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT  id,username,phone, picture, fullname, password,role, email"
            stmt += " FROM painters "
            stmt += "WHERE username={0} and verified=1"
            query = sql.SQL(stmt).format(sql.Literal(username))
            cursor.execute(query)
            user = cursor.fetchone()
            return user


def get_painters():
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT id,username,phone, picture, fullname,email, role, verified "
            stmt += "FROM painters"
            cursor.execute(stmt)
            painters = cursor.fetchall()
            painter = map(lambda p: PainterBase(*p).dict(), painters)
            return list(painter)


def get_profile(username):

    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT username, phone, picture, email,bio, facebook, instagram, x, tiktok, youtube,fullname "
            stmt += "FROM painters "
            stmt += "LEFT JOIN social_medias ON painters.id = social_medias.p_id "
            stmt += "WHERE painters.id = (SELECT id FROM painters WHERE username = {0})"
            query = sql.SQL(stmt).format(sql.Literal(username))
            cursor.execute(query)
            painter = cursor.fetchone()
            return {
                "username": painter[0],
                "phone": painter[1],
                "picture": painter[2],
                "email": painter[3],
                "bio": painter[4],
                "facebook": painter[5],
                "instagram": painter[6],
                "x": painter[7],
                "tiktok": painter[8],
                "youtube": painter[9],
                "fullname":painter[10]
            }
        



def get_profiles():

    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt = "SELECT username, phone, picture, email,bio, facebook, instagram, x, tiktok, youtube,fullname "
            stmt += "FROM painters "
            stmt += "LEFT JOIN social_medias ON painters.id = social_medias.p_id "
            # stmt += "WHERE painters.id = (SELECT id FROM painters WHERE username = {0})"
            query = sql.SQL(stmt)
            cursor.execute(query)
            profiles = cursor.fetchall()
            return [{
                "username": profile[0],
                "phone": profile[1],
                "picture": profile[2],
                "email": profile[3],
                "bio": profile[4],
                "facebook": profile[5],
                "instagram": profile[6],
                "x": profile[7],
                "tiktok": profile[8],
                "youtube": profile[9],
                "fullname":profile[10]
            }for profile in profiles ]



def delete_painter(id):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "DELETE FROM painters "
            stmt += "WHERE id ={0} "
            stmt += "RETURNING id,username,phone, picture, fullname,email"
            query = sql.SQL(stmt).format(sql.Literal(id))
            cursor.execute(query)
            deleted_painter = cursor.fetchall()
            cursor.execute("COMMIT")
            return deleted_painter


def update_painter(painter: PainterBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE painters "
            stmt += "SET username={0},phone={1}, picture={2}, fullname={3}, bio={4} "
            stmt += "WHERE id={5}"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get_username()),
                sql.Literal(painter.get_phone()),
                sql.Literal(painter.get_picture()),
                sql.Literal(painter.get_fullname()),
                sql.Literal(painter.get_bio()),
                sql.Literal(painter.get_id()),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            update_social_medias(painter)
            return True


def update_social_medias(painter: PainterBase):
    with contextlib.closing(get_db()) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("BEGIN")
            stmt = "UPDATE social_medias "
            stmt += "SET instagram={0},facebook={1}, x={2}, tiktok={3}, youtube={4} "
            stmt += "WHERE p_id={5}"
            query = sql.SQL(stmt).format(
                sql.Literal(painter.get_instagram()),
                sql.Literal(painter.get_facebook()),
                sql.Literal(painter.get_x()),
                sql.Literal(painter.get_tiktok()),
                sql.Literal(painter.get_youtube()),
                sql.Literal(painter.get_id()),
            )
            cursor.execute(query)
            cursor.execute("COMMIT")
            return True
