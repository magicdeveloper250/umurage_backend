class BlogBase:
    def __init__(self, id, title, content, created, author) -> None:
        self._id = id
        self._title = title
        self._content = content
        self._created = created
        self._author = author

    def get_id(self) -> str:
        return self._id

    def get_title(self) -> str:
        return self._title

    def get_content(self) -> str:
        return self._content

    def get_created(self) -> str:
        return self._created

    def get_author(self) -> str:
        return self._author

    @staticmethod
    def dict(object) -> dict:
        return {
            "id": object.get_id(),
            "title": object.get_title(),
            "content": object.get_content(),
            "created": object.get_created(),
            "author": object.get_author(),
        }
