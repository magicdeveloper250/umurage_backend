from flask import abort, request, redirect, Blueprint, jsonify, make_response
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from oauthlib.oauth2 import WebApplicationClient
from db.painter import get_painter_by_email
from flask import current_app
from models.user import User
from db.auth import get_user
from functools import wraps
import json, requests
import cryptocode
import datetime
import bcrypt
import jwt
from . import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_DISCOVERY_URL,
    SESSION_KEY,
    TOKEN_KEY,
    REFRESH_KEY,
    GOOGLE_REDIRECT_URL,
    SESSION_TIME,
)
from flask_login import (
    login_required,
    logout_user,
)
import os

auth = Blueprint(name="UserAuth", import_name="auth")
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route("/login222ejhfghghfhdghdete7t7337838368338686", methods=["GET"])
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
        return jsonify(
            {
                "success": False,
                "message": "User email not verified or not available on google",
            }
        )
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
        return jsonify(
            {
                "success": False,
                "message": "User email not verified or not available on google",
            }
        )
    return jsonify({"success": True, "token": token})


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    AFTER_LOGIN_URL = request.args.get("next")
    logout_user()
    return redirect(AFTER_LOGIN_URL, 302)


"""END OF GOOGLE LOGIN"""


"""CUSTOM LOGIN SYSTEM"""


def generate_access_token(payload):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=SESSION_TIME
    )
    token = jwt.encode(
        payload,
        TOKEN_KEY,
        algorithm="HS256",
    )
    return token


def generate_refresh_token(payload):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    token = jwt.encode(
        payload,
        REFRESH_KEY,
        algorithm="HS256",
    )
    return token


@auth.route("/custom-login", methods=["POST"])
def custom_login():
    username = request.form.get("username")
    password = request.form.get("password")
    error = None
    token = None
    if username and password:
        user = User.getByUsername(username)
        try:
            if not user:
                return (
                    jsonify(
                        {"success": False, "message": "username or password incorrect"}
                    ),
                    401,
                )
            if bcrypt.checkpw(password.encode(), user.password.encode()) == False:
                return (
                    jsonify(
                        {"success": False, "message": "username or password incorrect"}
                    ),
                    401,
                )
            else:
                token = generate_access_token(
                    {
                        "user": user.username,
                        "role": user.role,
                        "phone": user.phone,
                        "picture": user.picture,
                        "email": user.email,
                        "fullname": user.fullname,
                        "id": cryptocode.encrypt(user.id, SESSION_KEY),
                    }
                )
                refresh_token = generate_refresh_token(
                    {
                        "user": user.username,
                    }
                )
                response = make_response(jsonify({"success": True, "token": token}))
                response.set_cookie(
                    "refresh_token",
                    refresh_token,
                    max_age=24 * 60 * 60 * 1000,
                    samesite="lax",
                    secure=False,
                    httponly=True,  # Set max_age in seconds (1 day here)
                )
                return response

        except Exception as error:
            current_app.logger.warning(
                f"login attempt failed with this error {str(error)}"
            )
            return (
                jsonify({"success": False, "message": "uncaught error, try again"}),
                401,
            )
    else:
        current_app.logger.warning(
            f"login attempt failed with this error: no username and password provided"
        )
        return (
            jsonify({"success": False, "message": "username or password incorrect"}),
            401,
        )


@auth.route("/refresh", methods=["GET"])
def refresh_token():
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        payload = jwt.decode(
            refresh_token,
            REFRESH_KEY,
            algorithms=["HS256"],
        )

        if user := User.getByUsername(payload.get("user")):
            token = generate_access_token(
                {
                    "user": user.username,
                    "role": user.role,
                    "phone": user.phone,
                    "picture": user.picture,
                    "email": user.email,
                    "fullname": user.fullname,
                    "id": cryptocode.encrypt(user.id, SESSION_KEY),
                }
            )
            return jsonify({"success": True, "token": token}), 200
        else:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
    return jsonify({"success": False, "message": "Unauthorized"}), 401


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            key_from_request = request.headers.get("Authorization").split(" ")[1]
            payload = jwt.decode(key_from_request, TOKEN_KEY, algorithms=["HS256"])
            if dict(payload).get("role") != "admin":
                current_app.logger.warning(f"Action denied due to no admin privilege")
                return abort(jsonify({"message": False, "unauthorized": True}))
        except ExpiredSignatureError:
            return (
                jsonify(
                    {"success": False, "message": "Your session expired. Login again"}
                ),
                403,
            )
        except PyJWTError:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        except Exception as error:
            current_app.logger.warning(
                f"Action denied due to no admin privilege with this error {error}"
            )
            return jsonify({"success": False, "message": "unAuthorized"}), 401
        return f(*args, **kwargs)

    return decorated


# CUSTOM LOGIN SYSTEM HELPER FUNCTIONS


def custom_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            key_from_request = request.headers.get("Authorization").split(" ")[1]
            jwt.decode(key_from_request, TOKEN_KEY, algorithms=["HS256"])

        except ExpiredSignatureError:
            return (
                jsonify(
                    {"success": False, "message": "Your session expired. Login again"}
                ),
                403,
            )
        except PyJWTError:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        except Exception as error:
            current_app.logger.warning(
                f"Action denied due to no admin privilege with this error {str(error)}"
            )
            return jsonify({"success": False, "message": str(error)}), 401
        return f(*args, **kwargs)

    return decorated


@auth.route("/api/authorize/<userId>", methods=["POST", "GET"])
@admin_required
def authorize_user(userId):
    authorized = get_user(cryptocode.decrypt(userId, TOKEN_KEY))
    return jsonify({"message": True if authorized != None else False})



def payment_required_updated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from db.customer import check_payment
        try:
            id = request.args.get("key")
            exId = request.args.get("id")
            paid = check_payment(id, exId)
            if paid[0]:
                pass
            else:
                current_app.logger.warning(
                    f"Unauthorized user tried to access protected asset which require payment"
                )
                return jsonify(
                        {"message": False, "message": "Payment required"}
                    ), 402
                   
                

        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset which require payment with thiss error {error}"
            )
            return jsonify({"message": False, "message": "payment required"}, ),402
            
        return f(*args, **kwargs)

    return decorated


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
                        {"message": False, "message": "Payment required"},
                    ),
                    402,
                )

        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset which require payment with thiss error {error}"
            )
            return abort(
                jsonify({"message": False, "message": "payment required"}, 402)
            )
        return f(*args, **kwargs)

    return decorated


def user_or_admin_required():
    admin, user = (False, False)
    key_from_request = request.headers.get("Authorization").split(" ")[1]
    payload = jwt.decode(key_from_request, TOKEN_KEY, algorithms=["HS256"])
    if dict(payload).get("role") == "admin":
        admin = True
    elif dict(payload).get("role") == None:
        user = True
    if not (user or admin):
        current_app.logger.warning(
            f"Unauthorized user tried to access protected asset which requires registered user or admin"
        )
        return jsonify({"message": False, "message": "Unauthorized"}), 401
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
                return (
                    jsonify(
                        {"message": False, "message": "Unauthorized"},
                    ),
                    402,
                )

        except Exception as error:
            current_app.logger.warning(
                f"Unauthorized user tried to access protected asset with this error {error}"
            )
            return (
                jsonify(
                    {"message": False, "message": "Unauthorized"},
                ),
            ), 402

        return f(*args, **kwargs)

    return decorated


"""END CUSTOM LOGIN SYSTEM"""
