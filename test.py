import json, os, sqlite3, requests

from flask import Flask, request, redirect, url_for

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
from user_db import init_db_command
from user import User

GOOGLE_CLIENT_ID = (
    "673984937291-80v3d11ntqu1j6ji7tng9jf42ktr4tek.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# app setup
app = Flask(__name__)
app.secret_key = "673984937291"
loginmanager = LoginManager()
loginmanager.init_app(app)
try:
    init_db_command()
except sqlite3.OperationalError:
    pass
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@loginmanager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return "<p>hello, {} welcome to our web app and your email address is {} <img src='{}'/> </p> <br/><a href='/logout'><button>Logout</button></a>".format(
            current_user.name, current_user.email, current_user.profile_pic
        )
    else:
        return "<a href='/login'><button>Login with google.</button></a>"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login", methods=["GET"])
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # preparing request uri

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace("/login", "/login/callback"),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # preparing token request
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))
    user_info_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(user_info_endpoint)
    user_info_response = requests.get(uri, headers=headers, data=body)

    if user_info_response.json().get("email_verified"):
        uniqueid = user_info_response.json()["sub"]
        email = user_info_response.json()["email"]
        picture = user_info_response.json()["picture"]
        username = user_info_response.json()["given_name"]
    else:
        return "User email not verified or not available on google", 400

    user = User(uniqueid, username, email, picture)
    if not User.get(uniqueid):
        User.create(uniqueid, username, email, picture)
    login_user(user)
    return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")
