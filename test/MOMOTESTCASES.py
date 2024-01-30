import requests
import json

API_KEY = ""
API_SECRET = ""
callback_url = "https://webhook.site/70355654-c8b8-4072-b811-2e2da6647670"
momotokenurl = "https://sandbox.momodeveloper.mtn.com/collection/token/"
token_url = "https://sandbox.momodeveloper.mtn.com/apiuser"
REQUEST_TOpAY_URL = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
HOST = "sandbox.momodeveloper.mtn.com"
SUBSCRIPTION_KEY = "c4f44bafdc2946e79a2f38b609da9046"


def get_access_token():
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    user = requests.post(token_url, headers=headers)
    print(user)


def request_to_pay():
    print("requesting to pay")
    payload = {
        "amount": "500",
        "currency": "RWF",
        "externalId": "f8171f40-6078-4b6b-a972-3fa94f2af82c",
        "payer": {"partyIdType": "MSISDN", "partyId": "079"},
        "payerMessage": "you are going to pay",
        "payeeNote": "message from payer",
    }
    header = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
    }
    data = requests.post(REQUEST_TOpAY_URL)
    print(data)


get_access_token()
