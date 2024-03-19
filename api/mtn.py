from requests.exceptions import ConnectionError, ConnectTimeout
from payment.mtn import make_mtn_payment
from flask import request, jsonify
import db.customer as customer_db
import db.payment as database
from flask import Blueprint

mtn = Blueprint(name="mtn", import_name="mtn")


@mtn.route("/request_to_pay", methods=["POST"])
def pay_with_mtn():
    c_id = request.form.get("c_id")
    c_number = request.form.get("phonenumber")
    c_amount = request.form.get("amount")
    c_exhibition = request.form.get("ex_id")
    try:
        pid, status = make_mtn_payment(c_number, c_amount)
        payment_info = {
            "pay_for": c_exhibition,
            "pay_customer": c_id,
            "pay_value": c_amount,
            "pay_via": "MTN MOMO",
            "pay_phone_number": c_number,
        }
        database.add_payment(payment_info)
        customer_db.update_customer_status(c_id, "active")
        return jsonify(
            {
                "success": True,
                "status": status.get("status"),
                "message": "Transaction done successfully",
            }
        )
    except (
        ConnectionRefusedError,
        ConnectionError,
        ConnectionAbortedError,
        ConnectionResetError,
        ConnectTimeout,
    ):
        return jsonify({"success": False, "error": "server connection error"})

    except Exception as error:
        return jsonify({"success": False, "error": str(error)})
