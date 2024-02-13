from flask import Blueprint, request, jsonify, send_file
import db.painter as database
from helperfunctions import convertToObject
import os
from werkzeug.utils import secure_filename
import bcrypt
from auth.UserAuth import admin_required
from psycopg2 import IntegrityError
import threading

painter = Blueprint(name="painter", import_name="painter")


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
            + f"/images/painters/"
            + secure_filename(filename)
        )

        save_thread= threading.Thread(target=lambda:  profilepicture.save(
            os.path.join(os.getcwd() + f"/images/painters", secure_filename(filename))
        ))
        save_thread.start()
        database.add_new_painter(new_painter)
        return jsonify({"success": True})
    except IntegrityError:
         
        return jsonify({"userExist": True})
    except:
        return jsonify({"success": False})


@painter.route("/get_painters", methods=["GET"])
def list_painters():
    admin_required()
    try:
        painters = database.get_painters()
        headers = ["id", "username", "fullname", "phone", "image"]
        return jsonify(convertToObject(headers, painters))
    except Exception as error:
        print(error)


@painter.route("/delete_painter/<id>", methods=["DELETE"])
def delete_painter(id):
    admin_required()
    try:
        database.delete_painter(id)
        painters = database.get_painters()
        headers = ["id", "username", "fullname", "phone", "image"]
        return jsonify({"success": True, "data": convertToObject(headers, painters)})
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@painter.route("/images/painters/<filename>")
def send_painting(filename):
    fname = secure_filename(filename)
    file = os.path.join(os.getcwd() + "/images/painters", fname)
    return send_file(file)
