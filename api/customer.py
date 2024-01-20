from flask import jsonify, request, Blueprint, abort
import db.customer as database
from helperfunctions import convertToObject
from auth.UserAuth import admin_required
import send_email.customer as email
import threading

customer = Blueprint(name="customer", import_name="customer")

headers = [
    "id",
    "firstName",
    "lastName",
    "email",
    "phone",
    "exId",
    "exName",
    "status",
]


@customer.route("/add_customer", methods=["POST"])
def add_customer():
    header = [
        "id",
        "firstName",
        "lastName",
        "email",
        "phone",
        "exId",
        "status",
    ]

    try:
        customer = request.form
        added_customer = database.add_customer(customer)
        message = f"""
<div style='font-family:verdana; font-size:1.5rem'>
<b>EXHIBITION REGISTRATION INFO</b>
<p>Dear, thank you for registering to our exhibition.</p>
<p>Your customer id is <b>{added_customer[0][0]}<b/></p>
<em>Keep it safe, you will use it after payment<em/><br/>
 <em><b>Umurage art hub</b> </em>
</div>"""
        email_threading = threading.Thread(
            target=email.send_html_email,
            args=[
                customer.get("email"),
                "EXHIBITION REGISTRATION INFO",
                message,
            ],
        )
        email_threading.start()

        return jsonify(
            {
                "success": True,
                "data": convertToObject(header, added_customer),
            },
        )

    except Exception as error:
        print(error)
        return jsonify({"success": False})


@customer.route("/get_customers", methods=["GET"])
def get_customers():
    admin_required()
    try:
        customers = database.get_customers()

        return jsonify({"success": True, "data": convertToObject(headers, customers)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@customer.route("/update_customer_status", methods=["POST"])
def update_customer_status():
    admin_required()
    customer_id, current_status = request.form.get("customer_id"), request.form.get(
        "current_status"
    )
    try:
        new_status = "active" if current_status == "pending" else "pending"
        database.update_customer_status(customer_id, new_status)
        customers = database.get_customers()

        return jsonify({"success": True, "data": convertToObject(headers, customers)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@customer.route("/delete_customer", methods=["DELETE"])
def delete_customer():
    admin_required()
    customer_id = request.form.get("customer_id")
    try:
        database.delete_customer(customer_id)
        customers = database.get_customers()

        return jsonify({"success": True, "data": convertToObject(headers, customers)})

    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@customer.route("/get_customer/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = database.get_customers(id=id)
        headers = ["id", "firstName", "lastName", "phone", "email", "status"]
        return jsonify({"success": True, "data": convertToObject(headers, customer)})

    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@customer.route("/check_payment", methods=["POST"])
def check_payment():
    print("checking")
    try:
        id = request.form.get("customerId")
        exId = request.form.get("exhibitionId")
        response = database.check_payment(id=id, e_id=exId)
        print(response)
        if response:
            return jsonify({"success": True, "id": exId})
        else:
            return jsonify({"success": False, "error": False})
    except Exception as error:
        print(error)
        return jsonify({"success": False, "error": True})
