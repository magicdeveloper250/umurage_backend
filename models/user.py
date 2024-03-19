from flask_login import UserMixin
from models.painter import Painter


class User(UserMixin):
    def __init__(
        self,
        id,
        username,
        phone,
        picture,
        fullname,
        email,
        password=None,
        role=None,
    ):
        self.id = id
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.picture = picture
        self.phone = phone
        self.role = role

    @staticmethod
    def get(user_id):
        user = Painter.get_painter(user_id)
        if not user:
            return None
        else:
            user = User(
                id=user[0],
                username=user[1],
                phone=user[2],
                picture=user[3],
                fullname=user[4],
                email=user[7],
                password=user[5],
                role=user[6],
            )
            return user

    @staticmethod
    def getByUsername(username):
        user = Painter.get_user_by_username(username)

        if user:
            return User(
                id=user[0],
                username=user[1],
                phone=user[2],
                picture=user[3],
                fullname=user[4],
                email=user[7],
                password=user[5],
                role=user[6],
            )
        else:
            return None

    @staticmethod
    def create(
        id,
        username,
        phone,
        picture,
        fullname,
        email,
        password=None,
        role=None,
    ):
        painter = Painter(id, username, phone, picture, fullname, password, email)
        painter.add_painter()
