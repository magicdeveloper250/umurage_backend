from emails.email_verification_worker import EmailVerificationWorker
from psycopg2 import IntegrityError, DatabaseError, OperationalError
from auth.UserAuth import admin_required, custom_login_required
from flask import Blueprint, request, jsonify
from filemanagement import filemanager
from models.painter import Painter
from flask import current_app
import cryptocode
import bcrypt
import jwt
import os

painter = Blueprint(name="painter", import_name="painter")


@painter.route("/add_new_painter", methods=["POST"])
@admin_required
def add_new_painter():
    """ROUTE FOR ADDING NEW PAINTER ACCOUNT"""
    try:
        username = request.form.get("username")
        phone = request.form.get("phonenumber")
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        bio = request.form.get("bio")
        instagram = request.form.get("instagram")
        facebook = request.form.get("facebook")
        tiktok = request.form.get("tiktok")
        x = request.form.get("x")
        youtube = request.form.get("youtube")
        # hashing password from frontend to be saved in database
        hashedpw = bcrypt.hashpw(
            request.form.get("password").encode(), bcrypt.gensalt()
        )
        profilepicture = request.files.get("profilepicture")
        # saving user profile image to claudinary
        image_url = filemanager.add_user_profile_file(
            profilepicture, os.urandom(24).hex()
        )
        # instantiate new painter object with information from frontend
        new_painter = Painter(
            None,
            username,
            phone,
            image_url,
            fullname,
            email,
            None,
            0,
            password=str(hashedpw).removeprefix("b'").removesuffix("'"),
            bio=bio,
            instagram=instagram,
            facebook=facebook,
            tiktok=tiktok,
            youtube=youtube,
            x=x,
        )
        added_painter = (
            new_painter.add_painter()
        )  # adding new painter and return bool value
        base_url = request.base_url.removesuffix("/add_new_painter")
        # instantiate new email thread
        email_worker = EmailVerificationWorker(
            kwargs={
                "email": new_painter.get_email(),
                "painter_info": added_painter,
                "base_url": base_url,
            }
        )
        email_worker.start()  # start email send thread as deamon
        return jsonify({"success": True})
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "User already exist"}), 409
    except (DatabaseError, OperationalError) as error:
        current_app.logger.error(str(error))
        return (
            jsonify(
                {"success": False, "message": "Data submitted has an error, try again"}
            ),
            400,
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        print(error)
        return jsonify({"success": False, "message": "unknown error"}), 500


@painter.route("/update_painter", methods=["POST"])
@custom_login_required
def update_painter():
    """ROUTE FOR ADDING NEW PAINTER ACCOUNT"""
    try:
        username = request.form.get("username")
        phone = request.form.get("phonenumber")
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        bio = request.form.get("bio")
        instagram = request.form.get("instagram")
        facebook = request.form.get("facebook")
        tiktok = request.form.get("tiktok")
        x = request.form.get("x")
        youtube = request.form.get("youtube")
        profilepicture = request.files.get("profilepicture")
        image_url = None
        # use jwt library for decoding and validating token from email
        user = jwt.decode(
            request.headers.get("Authorization").split(" ")[1],
            os.environ.get("TOKEN_KEY"),
            algorithms=["HS256"],
        )
        # decrypting user id sent in an email
        user_id = cryptocode.decrypt(
            dict(user).get("id"), os.environ.get("SESSION_KEY")
        )

        if profilepicture:
            image_url = filemanager.add_user_profile_file(
                profilepicture, str(os.urandom(24).hex()) + "updated"
            )

        else:
            image_url = request.form.get("profilepicture")

        # instantiate new painter object with information from frontend
        painter = Painter(
            user_id,
            username,
            phone,
            image_url,
            fullname,
            email,
            role=None,
            verified=1,
            password=None,
            bio=bio,
            instagram=instagram,
            facebook=facebook,
            tiktok=tiktok,
            youtube=youtube,
            x=x,
        )
        painter_updated = painter.update_painter()

        return jsonify({"success": painter_updated})
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "User already exist"}), 409
    except (DatabaseError, OperationalError) as error:
        current_app.logger.error(str(error))
        return (
            jsonify(
                {"success": False, "message": "Data submitted has an error, try again"}
            ),
            500,
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500


@painter.route("/get_painters", methods=["GET"])
@admin_required
def list_painters():
    """ROUTE FOR GETTING LIST OF PAINTERS"""
    try:
        painters = Painter.get_painters()
        return jsonify({"success": True, "data": painters}), 200
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500


@painter.route("/change_password", methods=["POST"])
@custom_login_required
def change_password():
    """ROUTE FOR CHANGING PASSWORD"""
    try:
        # use jwt library for decoding and validating token from email
        user = jwt.decode(
            request.headers.get("Authorization").split(" ")[1],
            os.environ.get("TOKEN_KEY"),
            algorithms=["HS256"],
        )
        # decrypting user id sent in an email
        user_id = cryptocode.decrypt(
            dict(user).get("id"), os.environ.get("SESSION_KEY")
        )
        new_password = request.form.get("newPassword")
        # hash new password
        hashedpw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        # sanitize new password
        new_password = str(hashedpw).removeprefix("b'").removesuffix("'")
        Painter.change_password(user_id, new_password)
        return jsonify({"success": True, "message": "password changed"}), 200
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Invalid password"}), 400
    except (DatabaseError, OperationalError):
        return (
            jsonify(
                {"success": False, "message": "Data submitted has an error, try again"}
            ),
            400,
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500


@painter.route("/delete_painter/<id>", methods=["DELETE"])
@admin_required
def delete_painter(id):
    """ROUTE FOR DELETING PAINTER ACCOUNT"""
    try:
        Painter.delete_painter(id)
        painters = Painter.get_painters()
        return jsonify({"success": True, "data": painters})
    except (DatabaseError, OperationalError):
        return (
            jsonify(
                {"success": False, "message": "Data submitted has an error, try again"}
            ),
            400,
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500


@painter.route("/profile/<username>", methods=["GET"])
def get_profile(username):
    """ROUTE FOR GETTING painter profile"""
    try:
        profile = Painter.get_profile(username)
        return jsonify({"success": True, "data": profile}), 200
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500
    



@painter.route("/profiles", methods=["GET"])
def get_profiles():
    """ROUTE FOR GETTING all painters profiles"""
    try:
        profile = Painter.get_profiles()
        return jsonify({"success": True, "data": profile}), 200
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500
