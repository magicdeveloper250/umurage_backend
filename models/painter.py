from .painterbase import PainterBase
import db.painter as database


class Painter(PainterBase):
    def __init__(
        self,
        id,
        username,
        phone,
        picture,
        fullname,
        email,
        role=None,
        verified=0,
        password=None,
    ) -> None:
        super(Painter, self).__init__(
            id,
            username,
            phone,
            picture,
            fullname,
            email,
            role,
            verified,
            password,
        )

    def add_painter(self) -> bool:
        return database.add_new_painter(self)

    def update_painter(self) -> bool:
        return database.update_painter(self)

    @staticmethod
    def get_painters() -> list:
        return database.get_painters()

    @staticmethod
    def get_painter(painter_id) -> tuple:
        return database.get_painter(painter_id)

    @staticmethod
    def get_painter_by_email(email) -> tuple:
        return database.get_painter_by_email(email)

    @staticmethod
    def verify_email(painter_id, email) -> bool:
        return database.verify_email(painter_id, email)

    @staticmethod
    def get_user_by_username(username) -> tuple:
        return database.get_painter_by_username(username)

    @staticmethod
    def change_password(painter_id, new_password) -> bool:
        return database.change_password(painter_id, new_password)

    @staticmethod
    def delete_painter(painter_id) -> list:
        return database.delete_painter(painter_id)
