from .customerBase import CustomerBase
import db.customer as database


class Customer(CustomerBase):
    def __init__(
        self,
        id,
        c_first_name,
        c_last_name,
        c_email,
        c_phone,
        registered_for,
        exName=None,
        status="pending",
    ) -> None:
        super(Customer, self).__init__(
            id,
            c_first_name,
            c_last_name,
            c_email,
            c_phone,
            registered_for,
            exName,
            status,
        )

    def add_cutomer(self) -> dict:
        return database.add_customer(self)

    @staticmethod
    def get_customers(id=None) -> list:
        return database.get_customers(id)

    @staticmethod
    def update_customer_status(customer_id, new_status) -> bool:
        return database.update_customer_status(customer_id, new_status)

    @staticmethod
    def delete_customer(id) -> bool:
        return database.delete_customer(id)

    @staticmethod
    def check_payment(id, e_id) -> tuple:
        return database.check_payment(id, e_id)
