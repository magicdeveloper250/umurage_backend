from . import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_DISCOVERY_URL,
    SESSION_KEY,
    GOOGLE_REDIRECT_URL,
    GOOGLE_SUCCESS_LOGIN_REDIRECT,
    GOOGLE_FAILED_LOGIN_REDIRECT,
    SESSION_TIME,
)
from auth.user import User
from db.auth import get_user
from db.painter import get_painter_by_email
from flask import abort, request, redirect, Blueprint, jsonify, render_template
from flask import current_app
from flask_login import (
    LoginManager,
    login_required,
    logout_user,
)
from functools import wraps

from oauthlib.oauth2 import WebApplicationClient
import bcrypt
import cryptocode
import datetime
import json, requests
import jwt


auth = Blueprint(name="UserAuth", import_name="auth")
loginmanager = LoginManager()
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@loginmanager.user_loader
def load_user(user_id):
    return User.get(user_id)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route("/login", methods=["GET"])
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # preparing request uri
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=GOOGLE_REDIRECT_URL,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/callback")
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
    user = get_painter_by_email(email)
    token = jwt.encode(
        {
            "user": username,
            "role": None,
            "id": cryptocode.encrypt(uniqueid, SESSION_KEY),
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=SESSION_TIME),
            "picture": picture,
            "email": email,
        },
        SESSION_KEY,
    )
    if not user:
        return render_template("error.html", failed_url=GOOGLE_FAILED_LOGIN_REDIRECT)
    return render_template(
        "redirect.html", login_url=GOOGLE_SUCCESS_LOGIN_REDIRECT.format(token)
    )


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    AFTER_LOGIN_URL = request.args.get("next")
    logout_user()
    return redirect(AFTER_LOGIN_URL, 302)


"""END OF GOOGLE LOGIN"""


"""CUSTOM LOGIN SYSTEM"""


@auth.route("/custom-login", methods=["POST"])
def custom_login():
    username = request.form.get("username")
    password = request.form.get("password")
    error = None
    authorization_key = None
    if username and password:
        user = User.getByUsername(username)
        try:
            if not user:
                return jsonify({"message": False})
            if bcrypt.checkpw(password.encode(), user.password.encode()) == False:
                return jsonify({"message": False})
            else:
                authorization_key = jwt.encode(
                    {
                        "user": user.username,
                        "role": user.role,
                        "picture": user.picture,
                        "email": user.email,
                        "fullname": user.fullname,
                        "id": cryptocode.encrypt(user.id, SESSION_KEY),
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(minutes=SESSION_TIME),
                    },
                    SESSION_KEY,
                )

                return jsonify(
                    {
                        "message": True,
                        "token": authorization_key,
                    }
                )

        except Exception as error:
            current_app.logger.warning(
                f"login attempt failed with this error {str(error)}"
            )
            return jsonify({"message": False, "error": str(error)})

    else:
        current_app.logger.warning(f"login attempt failed with this error")
        return jsonify({"message": False})


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            key_from_request = request.headers.get("Authorization").split(" ")[1]
            payload = jwt.decode(key_from_request, SESSION_KEY, algorithms=["HS256"])
            if dict(payload).get("role") != "admin":
                current_app.logger.warning(f"Action denied due to no admin privilege")
                return abort(jsonify({"message": False, "unauthorized": True}))
        except Exception as error:
            current_app.logger.warning(
                f"Action denied due to no admin privilege with this error {error}"
            )
            return abort(jsonify({"message": False, "unauthorized": True}))
        return f(*args, **kwargs)

    return decorated


# CUSTOM LOGIN SYSTEM HELPER FUNCTIONS


def custom_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            key_from_request = request.headers.get("Authorization").split(" ")[1]
            jwt.decode(key_from_request, SESSION_KEY, algorithms=["HS256"])
        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset with this error {str(error)}"
            )
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )
        return f(*args, **kwargs)

    return decorated


@auth.route("/api/authorize/<userId>", methods=["POST", "GET"])
@admin_required
def authorize_user(userId):
    authorized = get_user(cryptocode.decrypt(userId, SESSION_KEY))

    return jsonify({"message": True if authorized != None else False})


def payment_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from db.customer import check_payment

        try:
            id = request.headers.get("clientId")
            exId = request.headers.get("exId")
            paid = check_payment(id, exId)
            if paid[0]:
                pass
            else:
                current_app.logger.warning(
                    f"Unauthorized user tried to access protected asset which require payment"
                )
                return abort(
                    jsonify(
                        {"message": False, "unauthorized": True},
                    )
                )

        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset which require payment with thiss error {error}"
            )
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )
        return f(*args, **kwargs)

    return decorated


def user_or_admin_required():
    admin, user = (False, False)
    key_from_request = request.headers.get("Authorization").split(" ")[1]
    payload = jwt.decode(key_from_request, SESSION_KEY, algorithms=["HS256"])
    if dict(payload).get("role") == "admin":
        admin = True
    elif dict(payload).get("role") == None:
        user = True
    if not (user or admin):
        current_app.logger.warning(
            f"Unauthorized user tried to access protected asset which requires registered user or admin"
        )
        return abort(jsonify({"message": False, "unauthorized": True}))
    return (user, admin)


def image_protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from db.customer import check_payment

        try:
            id = request.args.get("clientId")

            exId = request.args.get("exId")
            paid = check_payment(id, exId)
            if paid:
                pass
            else:
                current_app.logger.warning(
                    f"Unauthorized user tried to access protected image which requires payment"
                )
                return abort(
                    jsonify(
                        {"message": False, "unauthorized": True},
                    )
                )

        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset with this error {error}"
            )
            return abort(
                jsonify(
                    {"message": False, "unauthorized": True},
                )
            )
        return f(*args, **kwargs)

    return decorated


"""END CUSTOM LOGIN SYSTEM"""
