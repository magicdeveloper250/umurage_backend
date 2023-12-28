from flask_login import UserMixin

from db import painter as database


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        user = database.get_painter(user_id)
        print(user)
        if not user:
            return None
        else:
            user = User(id_=user[0], name=user[1], email=user[2], profile_pic=user[3])
            return user

    @staticmethod
    def getByUsername(username):
        user = database.get_painter_by_username(username)
        print(user)
        return User(id_=user[0], name=user[1], email=user[2], profile_pic=user[3])

    @staticmethod
    def create(id_, name, email, profile_pic):
        painter = {"id": id_, "username": name, "email": email, "picture": profile_pic}
        database.add_new_painter(painter)
