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
        bio=None,
        instagram=None,
        facebook=None,
        tiktok=None,
        youtube=None,
        x=None,
    ) -> None:
        self._id = id
        self._username = username
        self._phone = phone
        self._picture = picture
        self._fullname = fullname
        self._password = password
        self._email = email
        self._bio = bio
        self._facebook = facebook
        self._instagram = instagram
        self._tiktok = tiktok
        self._youtube = youtube
        self._x = x
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

    def get_bio(self) -> str:
        return self._bio

    def get_instagram(self) -> str:
        return self._instagram

    def get_facebook(self) -> str:
        return self._facebook

    def get_tiktok(self) -> str:
        return self._tiktok

    def get_youtube(self) -> str:
        return self._youtube

    def get_x(self) -> str:
        return self._x

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
