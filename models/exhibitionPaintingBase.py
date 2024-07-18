class ExhibitionPaintingBase:
    def __init__(self, id, name, description, image, audio, owner, painter) -> None:
        self._id = id
        self._name = name
        self._description = description
        self._image = image
        self._audio = audio
        self._owner = owner
        self._painter = painter

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_image(self) -> str:
        return self._image

    def get_audio(self) -> str:
        return self._audio

    def get_owner(self) -> str:
        return self._owner

    def get_painter(self) -> str:
        return self._painter

    def dict(cls) -> dict:
        return {
            "id": cls.get_id(),
            "name": cls.get_name(),
            "description": cls.get_description(),
            "image": cls.get_image(),
            "audio": cls.get_audio(),
            "owner": cls.get_owner(),
            "painter": cls.get_painter(),
        }
