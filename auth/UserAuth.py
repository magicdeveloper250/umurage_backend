import json, os, sqlite3, requests

from flask import (
    Flask,
    abort,
    make_response,
    request,
    redirect,
    url_for,
    Blueprint,
    current_app,
    jsonify,
    session,
)

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import os

from oauthlib.oauth2 import WebApplicationClient
from auth.user import User

GOOGLE_CLIENT_ID = (
    "673984937291-80v3d11ntqu1j6ji7tng9jf42ktr4tek.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
AFTER_LOGIN_URL = "http://localhost:5173/profile"
# app setup
auth = Blueprint(name="UserAuth", import_name="auth")

loginmanager = LoginManager()


@loginmanager.user_loader
def load_user(user_id):
    return User.get(user_id)


client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route("/login", methods=["GET"])
def login():
    AFTER_LOGIN_URL = request.args.get("next")
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # preparing request uri

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace("/login", "/login/callback"),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/login/callback")
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
    return redirect(AFTER_LOGIN_URL)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    AFTER_LOGIN_URL = request.args.get("next")
    logout_user()
    return redirect(AFTER_LOGIN_URL, 302)


# custom user authorization


@auth.route("/custom-login", methods=["POST"])
def custom_login():
    username = request.form.get("username")
    password = request.form.get("password")
    error = None
    authorization_key = None
    if username and password:
        # getting user from database

        user = User.getByUsername(username)
        if user:
            authorization_key = os.urandom(24).hex()

            login_user(user)

            return jsonify({"message": "success", "session": user.get_id()})
        else:
            error = "username or password is incorrect"
            return jsonify(message=error)
    else:
        error = "username and password required"
        return jsonify(message=error)


@auth.route("/custom-logout", methods=["GET"])
@login_required
def custom_logout():
    logout_user()
    return jsonify(success=True)


def custom_login_required():
    key_from_request = request.cookies.get("authorization_key")
    key_from_session = session.get("authorization_key")
    print(session.get("authorization_key"))
    print(request.cookies.get("authorization_key"))
    if key_from_request == key_from_session:
        print("access granted")
    else:
        return jsonify(abort(401))
