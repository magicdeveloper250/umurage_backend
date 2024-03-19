from .exhibitionBase import ExhibitionBase
import db.exhibition as database


class Exhibition(ExhibitionBase):
    def __init__(
        self,
        id,
        e_name,
        e_start_date,
        e_end_date,
        e_host,
        e_entrace_fees,
        e_banner,
    ) -> None:
        super(Exhibition, self).__init__(
            id, e_name, e_start_date, e_end_date, e_host, e_entrace_fees, e_banner
        )

    def add_exhibition(self) -> ExhibitionBase:
        return database.add_new_exhibition(self)

    @staticmethod
    def get_exhibition(ex_id) -> ExhibitionBase:
        return database.get_exhibition(ex_id)

    @staticmethod
    def get_exhibitions():
        return database.get_exhibitions()

    @staticmethod
    def delete_exhibition(ex_id) -> bool:
        return database.delete_exhibition(ex_id)

    def update_exhibition(self) -> bool:
        return database.update_exhibition(self)
