class ExhibitionBase:
    def __init__(
        self,
        id,
        e_name,
        e_start_date,
        e_end_date,
        e_host,
        e_entrace_fees,
        e_banner,
        status,
        description,
    ) -> None:
        self._name = e_name
        self._start_date = e_start_date
        self._end_date = e_end_date
        self._host = e_host
        self._fees = (e_entrace_fees,)
        self._banner = e_banner
        self._id = id
        self._status = status
        self._description = description

    def get_name(self) -> str:
        return self._name

    def get_start_date(self) -> str:
        return self._start_date

    def get_end_date(self) -> str:
        return self._end_date

    def get_fees(self):
        return self._fees

    def get_banner(self) -> str:
        return self._banner

    def get_host(self) -> str:
        return self._host

    def get_id(self) -> str:
        return self._id

    def get_status(self) -> str:
        return self._status

    def get_description(self) -> str:
        return self._description

    def dict(cls):
        return {
            "id": cls.get_id(),
            "name": cls.get_name(),
            "startdate": cls.get_start_date(),
            "enddate": cls.get_end_date(),
            "host": cls.get_host(),
            "fees": cls.get_fees(),
            "image": cls.get_banner(),
            "status": cls.get_status(),
            "description": cls.get_description(),
        }
