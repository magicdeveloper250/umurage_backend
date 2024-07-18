class CustomerBase:
    def __init__(
        self,
        id,
        c_first_name,
        c_last_name,
        c_email,
        c_phone,
        registered_for,
        exName,
        status="pending",
        datetime=None,
    ) -> None:
        self._id = id
        self._first_name = c_first_name
        self._lastname = c_last_name
        self._email = c_email
        self._phone = c_phone
        self._registered_for = registered_for
        self._status = status
        self._exname = exName
        self._datetime = datetime

    def get_id(self) -> str:
        return self._id

    def get_first_name(self) -> str:
        return self._first_name

    def get_last_name(self) -> str:
        return self._lastname

    def get_email(self) -> str:
        return self._email

    def get_phone(self) -> str:
        return self._phone

    def get_register_for(self):
        return self._registered_for

    def get_ex_name(self):
        return self._exname

    def get_status(self) -> str:
        return self._status

    def get_fullname(self) -> str:
        return self.get_first_name() + " " + self.get_last_name()

    def get_datetime(self) -> str:
        return self._datetime

    def dict(cls) -> dict:
        return {
            "id": cls.get_id(),
            "firstName": cls.get_first_name(),
            "lastName": cls.get_last_name(),
            "email": cls.get_email(),
            "phone": cls.get_phone(),
            "exId": cls.get_register_for(),
            "exName": cls.get_ex_name(),
            "status": cls.get_status(),
            "datetime": cls.get_datetime(),
        }
