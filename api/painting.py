from flask import Blueprint, request, abort, jsonify, send_file, make_response, g
import db.painting as database
from helperfunctions import convertToObject
import os
from werkzeug.utils import secure_filename
from auth.UserAuth import custom_login_required
from helperfunctions import authorize

painting = Blueprint(name="painting", import_name="painting")


@painting.route("/add_new_painting", methods=["PUT"])
def add_new_painting():
    try:
        new_painting = {}
        new_painting["name"] = request.form.get("name")
        new_painting["category"] = request.form.get("category")
        new_painting["owner"] = request.form.get("owner")
        image_file = request.files.get("painting")
        image_filename = (
            f"{request.form.get('owner')}" + "_painting_" + image_file.filename
        )
        new_painting["image"] = (
            request.base_url.replace("/add_new_painting", "")
            + "/images/paintings/"
            + secure_filename(image_filename)
        )
        database.add_new_painting(new_painting)
        image_file.save(
            os.path.join(
                os.getcwd() + "/images/paintings", secure_filename(image_filename)
            )
        )

        return jsonify({"success": True})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/get_paintings", methods=["GET", "POST"])
def get_paintings():
    try:
        painters = database.get_paintings()
        headers = ["id", "name", "owner", "category", "image", "phone"]

        return jsonify({"success": True, "data": convertToObject(headers, painters)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/images/paintings/<filename>")
def send_painting(filename):
    fname = secure_filename(filename)
    file = os.path.join(os.getcwd() + "/images/paintings", fname)
    return send_file(file)


@painting.route("/delete_painting/<id>", methods=["DELETE"])
def delete_painting(id):
    try:
        database.delete_painting(id)
        painters = database.get_paintings()
        headers = ["id", "name", "owner", "category", "image", "phone"]
        return jsonify({"success": True, "data": convertToObject(headers, painters)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/get_user_paintings/<id>", methods=["GET", "POST"])
def get_user_paintings(id):
    custom_login_required()
    try:
        painters = database.get_painting_by_id(id)
        headers = ["id", "name", "category", "image"]
        response = jsonify(
            {"success": True, "data": convertToObject(headers, painters)}
        )

        return response
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))
