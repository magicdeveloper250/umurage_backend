from flask import Blueprint
import requests
from flask import request, jsonify
import json
import base64
import logging
import db.payment as database
import db.customer as customer_database
from helperfunctions import convertToObject

payment = Blueprint(name="payment", import_name="payment")
logging.basicConfig(filename="./logging.log", filemode="a")
# REQUEST SETUP DATA
PAYPAL_CLIENT_ID = (
    "ATXE7I-Cou4tO1E9__yFBYMxdsx_p4cuzWTLd58CCBCRCl8kCLfyf2aOPptkY1xodLyYaicBMtWPaDC2"
)
PAYPAL_CLIENT_SECRET = (
    "EIQTb81lOWndJETP5hDje903u_mbWFVOJICbu_LGz4Nn0jjtfmWAnJbwhVhCjAiM2LxQGBTAsfyFOzjG"
)
BASE_URL = "https://api-m.sandbox.paypal.com"


def generate_access_token():
    """Getting token to use to access api"""
    AUTH_KEY = None
    if PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET is None:
        raise ValueError("MISSING API CREDINTIALS")
    else:
        AUTH_KEY = PAYPAL_CLIENT_ID + ":" + PAYPAL_CLIENT_SECRET
        encoded_credentials = base64.b64encode(AUTH_KEY.encode("utf-8")).decode("utf-8")
        response = requests.post(
            BASE_URL + "/v1/oauth2/token",
            headers={"Authorization": "Basic {0}".format(encoded_credentials)},
            data="grant_type=client_credentials",
        )

        logging.info("Access token created successfully")

        return response.json()["access_token"]


@payment.route("/api/payment/create-paypal-order", methods=["POST"])
def create_paypal_order():
    """Create an order to paypal"""
    product = request.form
    access_token = generate_access_token()
    url = f"{BASE_URL}/v2/checkout/orders"
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": f"{product.get('price')}",  # Replace with actual cart amount
                }
            }
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    # make order request
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(access_token),
        },
        json=payload,
    )

    return jsonify(response.json())


@payment.route("/api/payment/capture_order/<order_id>", methods=["POST"])
def capture_order(order_id):
    access_token = generate_access_token()
    url = "{0}/v2/checkout/orders/{1}/capture".format(BASE_URL, order_id)
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(access_token),
        },
    )

    logging.info("Transaction completed successfully.")

    return jsonify(response.json())


@payment.route("/confirm_payment", methods=["POST"])
def confirm_payment():
    order = request.form
    payment = {}
    payment["pay_for"] = order.get("exId")
    payment["pay_customer"] = order.get("c_id")
    payment["pay_value"] = order.get("price")
    payment["pay_via"] = "Paypal/Credit Card"
    payment["pay_phone_number"] = order.get("phone")
    try:
        database.add_payment(payment)
        customer_database.update_customer_status(order.get("c_id"), "active")
        return jsonify({"success": True})
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@payment.route("/delete_payment/<id>", methods=["POST"])
def delete_payment(id):
    try:
        database.delete_payments(id)
        headers = [
            "id",
            "exhibition",
            "customer",
            "amount",
            "time",
            "paid via",
            "phone",
        ]
        return jsonify(
            {"success": True, "data": convertToObject(headers, database.get_payments)}
        )
    except Exception as error:
        print(error)
        return jsonify({"success": False})
