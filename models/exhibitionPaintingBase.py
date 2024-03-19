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

    @staticmethod
    def dict(object) -> dict:
        return {
            "id": object.get_id(),
            "name": object.get_name(),
            "description": object.get_description(),
            "image": object.get_image(),
            "audio": object.get_audio(),
            "owner": object.get_owner(),
            "painter": object.get_painter(),
        }
