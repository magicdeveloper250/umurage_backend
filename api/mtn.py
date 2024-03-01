from flask import Blueprint
from flask import request, jsonify
from flask import current_app
from helperfunctions import convertToObject
from payment.mtn import make_mtn_payment
import db.payment as database
import db.customer as customer_db

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
    except Exception as error:
        return jsonify({"success": True, "error": str(error)})
