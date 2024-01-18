import json, os, sqlite3, requests
from db.auth import get_user
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
import bcrypt
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import os
import sqlite3
import contextlib
from oauthlib.oauth2 import WebApplicationClient
from auth.user import User
import cryptocode

GOOGLE_CLIENT_ID = (
    "673984937291-80v3d11ntqu1j6ji7tng9jf42ktr4tek.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
AFTER_LOGIN_URL = "https://www.umuragearthubf.onrender.com/profile"
SESSION_DB_URL = "session.sqlite"
SESSION_KEY = "1234567890"
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
        redirect_uri="https://www.umuragearthub.onrender.com/login/callback",
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
    return redirect(AFTER_LOGIN_URL + "/{0}".format(user.get_id(), SESSION_KEY))


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

        try:
            if not user:
                return jsonify({"message": False})
            if bcrypt.checkpw(password.encode(), user.password.encode()) == False:
                return jsonify({"message": False})
            else:
                authorization_key = os.urandom(24).hex()
                # adding user to the sessiondb
                with sqlite3.connect(SESSION_DB_URL) as connection:
                    with contextlib.closing(connection.cursor()) as cursor:
                        stmt = "SELECT * FROM session WHERE username=?"
                        cursor.execute(stmt, [user.name])
                        session_user = cursor.fetchone()
                        if session_user:
                            stmt = "DELETE FROM session WHERE username=?"
                            cursor.execute(stmt, [user.name])
                        stmt = "INSERT INTO session (session_id, username, auth_key, role) "
                        stmt += "VALUES (?,?,?,?)"
                        cursor.execute(
                            stmt, [user.id, user.name, authorization_key, user.role]
                        )

                return jsonify(
                    {
                        "message": True,
                        "session": cryptocode.encrypt(authorization_key, SESSION_KEY),
                        "userId": user.id,
                        "role": user.role,
                        "username": user.name,
                    }
                )

        except Exception as error:
            print(error)
            return jsonify({"message": False})

    else:
        return jsonify({"message": False})


@auth.route("/custom-logout", methods=["GET"])
def custom_logout():
    custom_login_required()
    key = request.headers.get("Authorization").split(" ")[1]
    with sqlite3.connect(SESSION_DB_URL) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            stmt = "delete from session where auth_key=?"
            cursor.execute(stmt, [cryptocode.decrypt(key, SESSION_KEY)])
    return jsonify(success=True)


@auth.route("/custom-admin-logout", methods=["GET"])
def custom_admin_logout():
    admin_required()
    key = request.headers.get("Authorization").split(" ")[1]
    with sqlite3.connect(SESSION_DB_URL) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            stmt = "SELECT * FROM session  "
            stmt += "WHERE auth_key=?"
            cursor.execute(stmt, [cryptocode.decrypt(key, SESSION_KEY)])
            ukey = cursor.fetchone()
            if ukey[3] != "admin":
                return abort(jsonify({"message": False, "unauthorized": True}))
            else:
                stmt = "DELETE FROM  session "
                stmt += "WHERE role=? AND auth_key=?"
                cursor.execute(stmt, ["admin", cryptocode.decrypt(key, SESSION_KEY)])
    return jsonify(success=True)


def admin_required():
    try:
        key_from_request = request.headers.get("Authorization").split(" ")[1]
        if not key_from_request:
            return abort(jsonify({"message": False}))
        else:
            return True
        with sqlite3.connect(SESSION_DB_URL) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt = "SELECT * FROM session  "
                stmt += "WHERE auth_key=?"
                cursor.execute(
                    stmt, [cryptocode.decrypt(key_from_request, SESSION_KEY)]
                )
                key = cursor.fetchone()
                if key[3] != "admin":
                    return abort(jsonify({"message": False, "unauthorized": True}))
    except Exception as error:
        print(error)
        return abort(jsonify({"message": False, "unauthorized": True}))


def custom_login_required():
    try:
        key_from_request = request.headers.get("Authorization").split(" ")[1]
        if not key_from_request:
            return abort(jsonify({"message": False}))
        key_from_request = key_from_request.strip()
        key = None
        # getting session auth key

        with sqlite3.connect(SESSION_DB_URL) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt = "SELECT auth_key FROM session  "
                stmt += "WHERE auth_key=?"
                cursor.execute(
                    stmt, [cryptocode.decrypt(key_from_request, SESSION_KEY)]
                )
                key = cursor.fetchone()
        if not key[0]:
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )
        else:
            pass
    except Exception:
        return abort(
            jsonify(
                {"message": False, "unauthorized": True},
            )
        )


@auth.route("/api/authorize/<userId>", methods=["POST", "GET"])
def authorize_user(userId):
    admin_required()
    authorized = get_user(userId)

    return jsonify({"message": True if authorized != None else False})


def payment_required():
    from db.customer import check_payment

    try:
        id = request.headers.get("clientId")
        exId = request.headers.get("exId")
        paid = check_payment(id, exId)
        if paid:
            pass
        else:
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )

    except Exception as error:
        print(error)
        return abort(
            jsonify(
                {"message": False, "unauthorized": True},
            )
        )


def image_protected():
    from db.customer import check_payment

    try:
        id = request.args.get("clientId")
        exId = request.args.get("exId")
        paid = check_payment(id, exId)
        if paid:
            pass
        else:
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )

    except Exception as error:
        print(error)
        return abort(
            jsonify(
                {"message": False, "unauthorized": True},
            )
        )
