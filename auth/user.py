from db import painter as database
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, phone, password=None, role=None):
        self.id = id_
        self.name = name
        self.email = email
        self.password = password
        self.profile_pic = profile_pic
        self.phone = phone
        self.role = role

    @staticmethod
    def get(user_id):
        user = database.get_painter(user_id)
        print(user)
        if not user:
            return None
        else:
            user = User(
                id_=user[0],
                name=user[1],
                email=user[2],
                profile_pic=user[3],
                role=user[5],
            )
            return user

    @staticmethod
    def getByUsername(username):
        user = database.get_painter_by_username(username)

        if user:
            return User(
                id_=user[0],
                name=user[1],
                email=user[2],
                phone=user[3],
                profile_pic=user[4],
                password=user[5],
                role=user[6],
            )
        else:
            return None

    @staticmethod
    def create(id_, name, email, profile_pic):
        painter = {"id": id_, "username": name, "email": email, "picture": profile_pic}
        database.add_new_painter(painter)
