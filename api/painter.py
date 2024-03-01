from auth.UserAuth import admin_required, custom_login_required
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from flask import current_app
from helperfunctions import convertToObject
from psycopg2 import IntegrityError
import bcrypt
import db.painter as database
import os
import emails.email_verification as email
import threading
import jwt
import cryptocode
from auth import SESSION_KEY

painter = Blueprint(name="painter", import_name="painter")
HEADERS = ["id", "username", "phone", "image", "fullname", "role", "email", "verified"]


@painter.route("/add_new_painter", methods=["POST"])
@admin_required
def add_new_painter():
    try:
        new_painter = {}
        id = os.urandom(24).hex()
        new_painter["id"] = id
        new_painter["email"] = request.form.get("email")
        new_painter["username"] = request.form.get("username")
        hashedpw = bcrypt.hashpw(
            request.form.get("password").encode(), bcrypt.gensalt()
        )
        new_painter["fullname"] = request.form.get("fullname")
        new_painter["password"] = str(hashedpw).removeprefix("b'").removesuffix("'")
        new_painter["phonenumber"] = request.form.get("phonenumber")
        profilepicture = request.files.get("profilepicture")
        image_url = filemanager.add_user_profile_file(profilepicture, new_painter["id"])
        new_painter["profilepicture"] = image_url
        added_painter = convertToObject(HEADERS, database.add_new_painter(new_painter))
        base_url = request.base_url.removesuffix("/add_new_painter")
        email_thread = threading.Thread(
            target=email.send_html_email,
            args=[new_painter["email"], added_painter[0], base_url],
        )
        email_thread.start()

        return jsonify({"success": True})
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"userExist": True})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})


@painter.route("/get_painters", methods=["GET"])
@admin_required
def list_painters():
    global HEADERS
    try:
        painters = database.get_painters()
        return jsonify(convertToObject(HEADERS, painters))
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@painter.route("/change_password", methods=["POST"])
@custom_login_required
def change_password():
    try:
        user = jwt.decode(
            request.headers.get("Authorization").split(" ")[1],
            SESSION_KEY,
            algorithms=["HS256"],
        )
        user_id = cryptocode.decrypt(dict(user).get("id"), SESSION_KEY)
        new_password = request.form.get("newPassword")
        hashedpw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        new_password = str(hashedpw).removeprefix("b'").removesuffix("'")
        database.change_password(user_id, new_password)
        return jsonify({"message": "password changed"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"error": str(error)})


@painter.route("/delete_painter/<id>", methods=["DELETE"])
@admin_required
def delete_painter(id):
    try:
        deleted_painter = database.delete_painter(id)
        painters = database.get_painters()
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})


@painter.route("/uploads/profiles/<filename>")
def send_painter_profile(filename):
    path = filemanager.get_user_profile_file_path(filename)
    return send_file(path)
