from .blogBase import BlogBase
import db.blog as database


class Blog(BlogBase):
    def __init__(self, id, title, content, created, author) -> None:
        super(Blog, self).__init__(id, title, content, created, author)

    def add_blog(self) -> list:
        database.add_blog(self)

    @staticmethod
    def get_blogs(id=None) -> list:
        return database.get_blogs(id=id)

    @staticmethod
    def delete_blog(id) -> bool:
        return database.delete_blog(id)
