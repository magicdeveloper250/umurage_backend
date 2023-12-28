from flask import Blueprint
import requests
from flask import request, jsonify
import json
import base64
import logging

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
                    "value": "100.00",  # Replace with actual cart amount
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
    # print(response.json())

    logging.info("Transaction completed successfully.")

    return jsonify(response.json())
