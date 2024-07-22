import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SESSION_DB_URL = os.environ.get("SESSION_DB_URL")
SESSION_KEY = os.environ.get("SESSION_KEY")
TOKEN_KEY = os.environ.get("TOKEN_KEY")
REFRESH_KEY = os.environ.get("REFRESH_KEY")
EMAIL_KEY = os.environ.get("EMAIL_KEY")
EXHIBITION_PAINTINGS_KEY = os.environ.get("EXHIBITION_PAINTINGS_KEY")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
AFTER_LOGIN_URL = "https://www.umuragearthubf.onrender.com/profile"
GOOGLE_REDIRECT_URL = "https://localhost:55555/callback"
GOOGLE_SUCCESS_LOGIN_REDIRECT = "http://localhost:5173/oprofile/?t={0}"
GOOGLE_FAILED_LOGIN_REDIRECT = "http://localhost:5173/sign-in"
AFTER_EMAIL_VERIFICATION_REDIRECT = "http://localhost:5173/sign-in"
SESSION_TIME = 2880
