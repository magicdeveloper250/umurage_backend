from auth.UserAuth import custom_login_required, user_or_admin_required
from filemanagement import filemanager
from flask import Blueprint, request, abort, jsonify, send_file
from helperfunctions import convertToObject
from werkzeug.utils import secure_filename
import db.painting as database
import os
import time

painting = Blueprint(name="painting", import_name="painting")

HEADERS = [
    "id",
    "name",
    "owner",
    "category",
    "created",
    "image",
    "phone",
    "likes",
]
MIN_HEADER = ["id", "name", "category", "image", "likes"]


@painting.route("/add_new_painting", methods=["PUT"])
def add_new_painting():
    global HEADERS
    try:
        new_painting = {}
        new_painting["name"] = request.form.get("name")
        new_painting["category"] = request.form.get("category")
        new_painting["owner"] = request.form.get("owner")
        image_file = request.files.get("painting")
        image_filename = (
            f"{request.form.get('owner')}"
            + "_painting_"
            + str(time.asctime()).replace(" ", "_")
            + image_file.filename.replace(" ", "_")
        )
        new_painting["image"] = (
            request.base_url.replace("/add_new_painting", "")
            + "/uploads/paintings/"
            + secure_filename(image_filename)
        )
        added_painting = database.add_new_painting(new_painting)
        filemanager.add_user_painting_file(image_file, image_filename)

        return jsonify(
            {"success": True, "data": convertToObject(HEADERS, added_painting)}
        )
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/get_paintings", methods=["GET", "POST"])
def get_paintings():
    global HEADERS
    try:
        painters = database.get_paintings()
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/uploads/paintings/<filename>")
def send_painting_file(filename):
    path = filemanager.get_user_painting_file_path(filename)
    return send_file(path)


@painting.route("/delete_painting/<id>", methods=["DELETE"])
def delete_painting(id):
    global HEADERS, min_HEADERS
    user, admin = user_or_admin_required()
    userId = request.headers.get("userId")
    try:
        deleted_painting = database.delete_painting(id, userId)
        filemanager.delete_user_painting_file(deleted_painting[0][5])
        painters = (
            database.get_painting_by_id(userId)
            if not admin
            else database.get_paintings()
        )
        HEADERS = MIN_HEADER if not admin else HEADERS
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/get_user_paintings/<id>", methods=["GET", "POST"])
def get_user_paintings(id):
    custom_login_required()
    try:
        painters = database.get_painting_by_id(id)
        HEADERS = ["id", "name", "category", "image", "likes"]
        response = jsonify(
            {"success": True, "data": convertToObject(HEADERS, painters)}
        )

        return response
    except Exception as error:
        return abort(jsonify({"success": False}))


@painting.route("/like/<painting_id>", methods=["POST"])
def like(painting_id):
    try:
        liked = database.like(painting_id)
        if liked:
            likes = database.get_likes(painting_id)
            print(likes)
            return jsonify({"success": True, "likes": likes[0]})
        else:
            return jsonify(
                {
                    "success": False,
                }
            )
    except Exception as error:
        return jsonify({"success": False, "error": error})


@painting.route("/dislike/<painting_id>", methods=["POST"])
def dislike(painting_id):
    try:
        liked = database.dislike(painting_id)
        if liked:
            likes = database.get_likes(painting_id)
            return jsonify({"success": True, "likes": likes[0]})
        else:
            return jsonify(
                {
                    "success": False,
                }
            )
    except Exception as error:
        return jsonify({"success": False, "error": error})
