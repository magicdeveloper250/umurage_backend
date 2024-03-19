from emails.customer_email_worker import CustomerEmailWorker
from flask import jsonify, request, Blueprint, abort
from auth.UserAuth import admin_required
from models.customer import Customer
from flask import current_app
from psycopg2.errors import (
    InvalidTextRepresentation,
    DatabaseError,
    OperationalError,
)

customer = Blueprint(name="customer", import_name="customer")


@customer.route("/add_customer", methods=["POST"])
def add_customer():
    """ROUTE FOR ADDING CUSTOMER"""
    try:
        data = request.form
        customer = Customer(
            None,
            data.get("firstname"),
            data.get("lastName"),
            data.get("email"),
            data.get("phonenumber"),
            data.get("exhibition"),
            None,
        )
        added_customer = customer.add_cutomer()
        email_worker = CustomerEmailWorker(
            kwargs={
                "email": customer.get_email(),
                "message": [added_customer["exId"], added_customer["id"]],
            }
        )
        email_worker.start()
        return jsonify(
            {
                "success": True,
                "data": [added_customer],
            },
        )
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@customer.route("/get_customers", methods=["GET"])
@admin_required
def get_customers():
    """ROUTE FOR GETTING CUSTOMERS"""
    try:
        return jsonify({"success": True, "data": Customer.get_customers(id=None)})
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has an error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@customer.route("/update_customer_status", methods=["POST"])
@admin_required
def update_customer_status():
    customer_id, current_status = request.form.get("customer_id"), request.form.get(
        "current_status"
    )
    try:
        new_status = "active" if current_status == "pending" else "pending"
        Customer.update_customer_status(customer_id, new_status)
        customers = Customer.get_customers()
        return jsonify({"success": True, "data": customers})
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@customer.route("/delete_customer", methods=["DELETE"])
@admin_required
def delete_customer():
    """ROUTE FOR DELETING CUSSTOMER"""
    customer_id = request.form.get("customer_id")
    try:
        Customer.delete_customer(customer_id)
        customers = Customer.get_customers()
        return jsonify({"success": True, "data": customers})
    except Exception as error:
        current_app.logger.error(str(error))
        return abort(jsonify({"success": False}))


@customer.route("/get_customer/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.get_customers(id=customer_id)
        return jsonify({"success": True, "data": customer})
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@customer.route("/check_payment", methods=["POST"])
def check_payment():
    """ROUTE FOR CHECKING PAYMENT"""
    try:
        id = request.form.get("customerId")
        exId = request.form.get("exhibitionId")
        response = Customer.check_payment(id=id, e_id=exId)
        if response:
            return jsonify({"success": True, "id": exId, "c_id": response[1]})
        else:
            return jsonify(
                {
                    "success": False,
                    "message": "You haven't enrolled to attend this exhibition",
                }
            )
    except InvalidTextRepresentation:
        return jsonify({"ssuccess": False, "message": "Invalid key"})
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})
