from .paintingBase import PaintingBase
import db.painting as database


class Painting(PaintingBase):
    def __init__(self, name, category, owner, created, image) -> None:
        super(Painting, self).__init__(name, category, owner, created, image)

    def add_painting(self) -> list:
        return database.add_new_painting(self)

    @staticmethod
    def get_paintings() -> list:
        return database.get_paintings()

    @staticmethod
    def get_user_paintings(userId) -> list:
        return database.get_painting_by_id(userId)

    @staticmethod
    def like(painting_id) -> bool:
        return database.like(painting_id)

    @staticmethod
    def get_likes(painting_id) -> tuple:
        return database.get_likes(painting_id)

    @staticmethod
    def dislike(painting_id) -> bool:
        return database.dislike(painting_id)

    @staticmethod
    def delete_painting(painting_id) -> bool:
        return database.delete_painting(painting_id)
