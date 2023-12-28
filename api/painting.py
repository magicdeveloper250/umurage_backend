from flask import Blueprint, request, jsonify, send_file, make_response, g
import db.painting as database
from flask_login import login_required
from helperfunctions import convertToObject
import os
from werkzeug.utils import secure_filename

# from auth.UserAuth import authorize
from helperfunctions import authorize

painting = Blueprint(name="painting", import_name="painting")


@painting.route("/add_new_painting", methods=["PUT"])
def add_new_painting():
    new_painting = {}
    new_painting["name"] = request.form.get("name")
    new_painting["category"] = request.form.get("category")
    image_file = request.files.get("painting")
    image_filename = (
        "4bbb5d19-4dee-40d8-a2d8-1b75da3e9d01" + "_painting_" + image_file.filename
    )
    new_painting["image"] = (
        request.base_url.replace("/add_new_painting", "")
        + "/images/paintings/"
        + image_filename
    )
    database.add_new_painting(new_painting)
    image_file.save(os.path.join(os.getcwd() + "/images/paintings", image_filename))

    return jsonify({"success": True})


@painting.route("/get_paintings", methods=["GET", "POST"])
# login_required
def get_paintings():
    user_id = request.form.get("user_id")
    auth_key = request.form.get("auth_key")

    # authorized = authorize(
    #     user_id, auth_key, flask.session.get("user_id"), flask.session.get("auth_key")
    # )
    # print(authorized)
    # if authorized:
    painters = database.get_paintings()
    headers = ["id", "name", "owner", "category", "image", "phone"]
    response = make_response(jsonify(convertToObject(headers, painters)))

    return response
    # else:
    #     return jsonify("Access denied")


@painting.route("/images/paintings/<filename>")
def send_painting(filename):
    fname = secure_filename(filename)
    file = os.path.join(os.getcwd() + "/images/paintings", fname)
    return send_file(file)
