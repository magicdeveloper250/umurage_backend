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
    ) -> None:
        self._name = e_name
        self._start_date = e_start_date
        self._end_date = e_end_date
        self._host = e_host
        self._fees = (e_entrace_fees,)
        self._banner = e_banner
        self._id = id
        self._status = status

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

    @staticmethod
    def dict(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "startdate": self.get_start_date(),
            "enddate": self.get_end_date(),
            "host": self.get_host(),
            "fees": self.get_fees(),
            "image": self.get_banner(),
            "status": self.get_status(),
        }
