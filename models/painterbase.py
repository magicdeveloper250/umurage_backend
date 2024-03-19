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

    @staticmethod
    def dict(object) -> dict:
        return {
            "id": object.get_id(),
            "username": object.get_username(),
            "phone": object.get_phone(),
            "image": object.get_picture(),
            "fullname": object.get_fullname(),
            "role": object.get_role(),
            "password": object.get_password(),
            "email": object.get_email(),
            "verified": object.get_verified(),
        }
