class PainterBase:
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
        self._id = id
        self._username = username
        self._phone = phone
        self._picture = picture
        self._fullname = fullname
        self._password = password
        self._email = email
        self._role = role
        self._verified = verified

    def get_id(self) -> str:
        return self._id

    def set_image(self, value):
        self._picture = value

    def get_username(self) -> str:
        return self._username

    def get_phone(self) -> str:
        return self._phone

    def get_picture(self) -> str:
        return self._picture

    def get_fullname(self) -> str:
        return self._fullname

    def get_email(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def get_role(self) -> str:
        return self._role

    def get_verified(self) -> str:
        return self._verified

    def dict(cls) -> dict:
        return {
            "id": cls.get_id(),
            "username": cls.get_username(),
            "phone": cls.get_phone(),
            "image": cls.get_picture(),
            "fullname": cls.get_fullname(),
            "role": cls.get_role(),
            "password": cls.get_password(),
            "email": cls.get_email(),
            "verified": cls.get_verified(),
        }
