class CommentBase:
    def __init__(self, id: str, ex_id: str, cust_id: str, text: str) -> None:
        self._id = id
        self._ex_id = ex_id
        self._cust_id = cust_id
        self._text = text

    def get_id(self) -> str:
        return self._id

    def get_ex_id(self) -> str:
        return self._ex_id

    def get_cust_id(self) -> str:
        return self._cust_id

    def get_text(self) -> str:
        return self._text

    def dict(cls) -> dict:
        return {
            "id": cls.get_id(),
            "ex_id": cls.get_ex_id(),
            "cust_id": cls.get_cust_id(),
            "text": cls.get_text(),
        }
