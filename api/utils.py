import requests
import os


def check_payment(tx_id):
    url = os.environ.get("FLUTTERWAVE_BASE_URL") + f"/transactions/{tx_id}/verify"
    headers = {
        "Authorization": f'Bearer {os.environ.get("FLUTTEWAVE_SECRET_KEY")}',
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data.get("status") == "success":
        payment_status = response_data["data"]["status"]
        if payment_status == "successful":
            return True, "Payment verified successfully"
        else:
            return False, "Payment not successful"
    else:
        return False, "Failed to verify payment"
