from auth.UserAuth import admin_required
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from helperfunctions import convertToObject
from psycopg2 import IntegrityError
from werkzeug.utils import secure_filename
import bcrypt
import db.painter as database
import os

painter = Blueprint(name="painter", import_name="painter")
HEADERS = ["id", "username", "fullname", "phone", "image"]


@painter.route("/add_new_painter", methods=["POST"])
def add_new_painter():
    # admin_required()
    try:
        new_painter = {}
        id = os.urandom(24).hex()
        new_painter["id"] = id
        new_painter["email"] = request.form.get("fullname")
        new_painter["username"] = request.form.get("username")
        hashedpw = bcrypt.hashpw(
            request.form.get("password").encode(), bcrypt.gensalt()
        )
        new_painter["password"] = str(hashedpw).removeprefix("b'").removesuffix("'")
        new_painter["phonenumber"] = request.form.get("phonenumber")
        profilepicture = request.files.get("profilepicture")
        filename = (
            request.form.get("username") + "_profilepicture_" + profilepicture.filename
        )

        new_painter["profilepicture"] = (
            request.base_url.replace("/add_new_painter", "")
            + f"/uploads/profiles/"
            + secure_filename(filename)
        )
        database.add_new_painter(new_painter)
        filemanager.add_user_profile_file(profilepicture, filename)
        return jsonify({"success": True})
    except IntegrityError as error:
        print(error)
        return jsonify({"userExist": True})
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@painter.route("/get_painters", methods=["GET"])
def list_painters():
    global HEADERS
    admin_required()
    try:
        painters = database.get_painters()
        return jsonify(convertToObject(HEADERS, painters))
    except Exception as error:
        print(error)


@painter.route("/delete_painter/<id>", methods=["DELETE"])
def delete_painter(id):
    admin_required()
    try:
        deleted_painter = database.delete_painter(id)
        painters = database.get_painters()
        filemanager.delete_user_profile_file(deleted_painter[0][4])
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@painter.route("/uploads/profiles/<filename>")
def send_painter_profile(filename):
    path = filemanager.get_user_profile_file_path(filename)
    return send_file(path)
