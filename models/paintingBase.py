class PaintingBase:
    def __init__(self, name, category, owner, created, image) -> None:
        self._name = name
        self._category = category
        self._owner = owner
        self._created = created
        self._image = image

    def get_name(self) -> str:
        return self._name

    def get_category(self) -> str:
        return self._category

    def get_owner(self) -> str:
        return self._owner

    def get_created(self) -> str:
        return self._created

    def get_image(self) -> str:
        return self._image

    def __repr__(self) -> str:
        return f"""
        name:{self.get_name()},
        category:{self.get_category()}, 
        owner:{self.get_owner()}, 
        image: {self.get_created()}, 
        image:{self.get_image()}"""

    def __str__(self) -> str:
        return self.__repr__()
