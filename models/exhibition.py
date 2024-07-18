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
        status,
    ) -> None:
        super(Exhibition, self).__init__(
            id,
            e_name,
            e_start_date,
            e_end_date,
            e_host,
            e_entrace_fees,
            e_banner,
            status,
        )

    def add_exhibition(self) -> ExhibitionBase:
        return database.add_new_exhibition(self)

    @staticmethod
    def get_exhibition(ex_id) -> ExhibitionBase:
        print(database.get_exhibition(ex_id))
        return database.get_exhibition(ex_id)

    @staticmethod
    def get_exhibitions():
        return database.get_exhibitions()

    @staticmethod
    def get_active_exhibitions():
        return database.get_active_exhibitions()

    @staticmethod
    def delete_exhibition(ex_id) -> bool:
        return database.delete_exhibition(ex_id)

    @staticmethod
    def change_exhibition_status(id, new_status) -> dict:
        return database.change_exhibition_status(id, new_status)

    def update_exhibition(self) -> bool:
        return database.update_exhibition(self)

    @staticmethod
    def get_pending_exhibitions() -> list:
        return database.get_pending_exhibitions()
