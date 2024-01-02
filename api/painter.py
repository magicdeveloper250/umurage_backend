from flask import Blueprint, request, jsonify, send_file
import db.painter as database
from helperfunctions import convertToObject
import os
from werkzeug.utils import secure_filename
import os
import bcrypt

painter = Blueprint(name="painter", import_name="painter")


@painter.route("/add_new_painter", methods=["POST"])
def add_new_painter():
    new_painter = {}
    id = os.urandom(24).hex()
    new_painter["id"] = id
    new_painter["email"] = request.form.get("fullname")
    new_painter["username"] = request.form.get("username")
    hashedpw = bcrypt.hashpw(request.form.get("password").encode(), bcrypt.gensalt())
    new_painter["password"] = str(hashedpw).removeprefix("b'").removesuffix("'")
    new_painter["phonenumber"] = request.form.get("phonenumber")
    profilepicture = request.files.get("profilepicture")
    filename = (
        request.form.get("username") + "_profilepicture_" + profilepicture.filename
    )

    new_painter["profilepicture"] = filename

    profilepicture.save(
        os.path.join(os.getcwd() + f"/images/painters", secure_filename(filename))
    )
    database.add_new_painter(new_painter)
    return jsonify({"success": True})


@painter.route("/get_painters", methods=["GET"])
def list_painters():
    painters = database.get_painters()
    headers = ["id", "username", "phone", "email", "phone"]
    return jsonify(convertToObject(headers, painters))


@painter.route("/delete_painter/<id>", methods=["DELETE"])
def delete_painter(id):
    try:
        database.delete_painter(id)
        painters = database.get_painters()
        headers = ["id", "username", "phone", "email", "phone"]
        return jsonify({"success": True, "data": convertToObject(headers, painters)})
    except Exception as error:
        print(error)
        return jsonify({"success": False})
