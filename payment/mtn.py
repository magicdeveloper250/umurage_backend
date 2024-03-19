from . import (
    MOMO_BASE_URL,
    MTN_CALLBACK_URL,
    SUBSCRIPTION_KEY,
    MTN_ENVIRONMENT,
    CURRENCY,
    MTN_PAYER_MESSAGE,
    MTN_PAYEE_MESSAGE,
)
import requests
import json
import uuid
import os


def create_user():
    reference_id = str(uuid.uuid4())
    headers = {
        "X-Reference-Id": reference_id,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
    }
    payload = json.dumps({"providerCallbackHost": MTN_CALLBACK_URL})
    response = requests.request(
        "POST", MOMO_BASE_URL + "/v1_0/apiuser", headers=headers, data=payload
    )
    if response.status_code == 201:
        return response, reference_id
    return False


def get_created_user(user_reference_id):
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    response = requests.request(
        "GET", MOMO_BASE_URL + f"/v1_0/apiuser/{user_reference_id}", headers=headers
    )
    if response.status_code == 200:
        return response.json()
    return False


def get_user_apikey(user_reference_id):
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    response = requests.request(
        "POST",
        MOMO_BASE_URL + f"/v1_0/apiuser/{user_reference_id}/apikey",
        headers=headers,
    )
    if response.status_code == 201:
        return dict(response.json()).get("apiKey")
    return False


def get_access_token(username, password):
    """Uses x-reference-id as username and apiKey as password"""
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    response = requests.request(
        "POST",
        MOMO_BASE_URL + f"/collection/token/",
        headers=headers,
        auth=(username, password),
    )
    if response.status_code == 200:
        return dict(response.json()).get("access_token")
    return False


def request_to_pay(access_token, phonenumber: str, amount: str):
    payment_id = str(uuid.uuid4())
    payment_headers = {
        "X-Reference-Id": payment_id,
        "X-Target-Environment": MTN_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = json.dumps(
        {
            "amount": amount,
            "currency": CURRENCY,
            "externalId": os.urandom(24).hex(),
            "payer": {"partyIdType": "MSISDN", "partyId": phonenumber},
            "payerMessage": MTN_PAYER_MESSAGE,
            "payeeNote": MTN_PAYEE_MESSAGE,
        }
    )
    response = requests.request(
        "POST",
        MOMO_BASE_URL + "/collection/v1_0/requesttopay",
        headers=payment_headers,
        data=payload,
    )
    if response.status_code == 202:
        return True, payment_id
    return False


def get_transaction_status(access_token, payment_id):
    headers = {
        "X-Target-Environment": MTN_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request(
        "GET",
        MOMO_BASE_URL + f"/collection/v1_0/requesttopay/{payment_id}",
        headers=headers,
    )
    return response.json()


def get_collection_account_balance(access_token):
    headers = {
        "X-Target-Environment": MTN_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request(
        "GET", MOMO_BASE_URL + "/collection/v1_0/account/balance", headers=headers
    )
    return response.json()


def get_account_holder_status(access_token, id_type, account_id):
    headers = {
        "X-Target-Environment": MTN_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request(
        "GET",
        MOMO_BASE_URL + f"/collection/v1_0/accountholder/{id_type}/{account_id}/active",
        headers=headers,
    )
    return response.json()


def make_mtn_payment(mobile_number, amount):
    response, user_id = create_user()
    created_user = get_created_user(user_id)
    user_api_key = get_user_apikey(user_id)
    access_token = get_access_token(user_id, user_api_key)
    account_holder_status = get_account_holder_status(
        access_token, "msisdn", mobile_number
    )
    if account_holder_status.get("result"):
        payment_requested, payment_id = request_to_pay(
            access_token, mobile_number, amount
        )
    else:
        raise ValueError("Number is not registered in mobile money")
    transaction_status = get_transaction_status(access_token, payment_id)

    if transaction_status.get("status") == "SUCCESSFUL":
        return (
            payment_id,
            transaction_status,
        )
    else:
        raise ValueError("Payment failed")
