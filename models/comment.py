from .commentBase import CommentBase
import db.comment as database


class Comment(CommentBase):
    def __init__(
        self,
        id: str,
        ex_id: str,
        cust_id: str,
        text: str,
    ) -> None:
        super(Comment, self).__init__(
            id,
            ex_id,
            cust_id,
            text,
        )

    def add_comment(self) -> bool:
        database.add_comment(self)

    @staticmethod
    def get_comments() -> list:
        database.get_comments()

    @staticmethod
    def delete_comment(id) -> bool:
        database.delete_comment(id)
