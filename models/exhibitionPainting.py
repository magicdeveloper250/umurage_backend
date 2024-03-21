from .exhibitionPaintingBase import ExhibitionPaintingBase
import db.exhibition_paintings as database


class ExhibitionPainting(ExhibitionPaintingBase):
    def __init__(self, id, name, description, image, audio, owner, painter) -> None:
        super(ExhibitionPainting, self).__init__(
            id, name, description, image, audio, owner, painter
        )

    def add_exhibition_painting(self) -> bool:
        return database.add_exhibition_paintings(self)

    @staticmethod
    def get_all_paintings() -> list:
        return database.get_all_exhibition_painting()

    @staticmethod
    def delete_exhibition_painting(id) -> bool:
        return database.delete_xhibition_painting(id)

    @staticmethod
    def get_exhibition_painting(ex_id) -> list:
        return database.get_exhibition_painting(ex_id)
