import os

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET")
BASE_URL = "https://api-m.sandbox.paypal.com"
MOMO_BASE_URL = "https://sandbox.momodeveloper.mtn.com"
MTN_CALLBACK_URL = "https://webhook.site/9dffd7a4-2b48-48bd-8c9c-52bf228677f2"
SUBSCRIPTION_KEY = os.environ.get("MTN_SUBSCRIPTION_KEY")
MTN_ENVIRONMENT = "sandbox"
CURRENCY = "EUR"
MTN_PAYER_MESSAGE = "You paid"
MTN_PAYEE_MESSAGE = "payine notice"
