from flask import jsonify, request, Blueprint, abort
import db.customer as database
from helperfunctions import convertToObject
from auth.UserAuth import admin_required

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
    try:
        id = request.form.get("customerId")
        exId = request.form.get("exhibitionId")
        response = database.check_payment(id=id, e_id=exId)
        if response:
            return jsonify({"success": True, "id": exId})
        else:
            return jsonify({"success": False})
    except Exception as error:
        print(error)
        return jsonify({"success": False})
