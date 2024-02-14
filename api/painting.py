from auth.UserAuth import custom_login_required, admin_required
from flask import Blueprint, request, abort, jsonify, send_file
from helperfunctions import convertToObject
from werkzeug.utils import secure_filename
import db.painting as database
import os
import time

painting = Blueprint(name="painting", import_name="painting")

headers = [
    "id",
    "name",
    "owner",
    "category",
    "created",
    "image",
    "phone",
    "likes",
]


@painting.route("/add_new_painting", methods=["PUT"])
def add_new_painting():
    global headers
    try:
        new_painting = {}
        new_painting["name"] = request.form.get("name")
        new_painting["category"] = request.form.get("category")
        new_painting["owner"] = request.form.get("owner")
        image_file = request.files.get("painting")
        image_filename = (
            f"{request.form.get('owner')}"
            + "_painting_"
            + str(time.asctime())
            + image_file.filename.replace(" ", "_")
        )
        new_painting["image"] = (
            request.base_url.replace("/add_new_painting", "")
            + "/images/paintings/"
            + secure_filename(image_filename)
        )
        added_painting = database.add_new_painting(new_painting)
        image_file.save(
            os.path.join(
                os.getcwd() + "/images/paintings", secure_filename(image_filename)
            )
        )

        return jsonify(
            {"success": True, "data": convertToObject(headers, added_painting)}
        )
    except Exception as error:
        print(error)
        return abort(jsonify({"success": False}))


@painting.route("/get_paintings", methods=["GET", "POST"])
def get_paintings():
    global headers
    try:
        painters = database.get_paintings()
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
    global headers
    custom_login_required()
    admin = admin_required()
    userId = request.headers.get("userId")
    try:
        database.delete_painting(id, userId)
        painters = (
            database.get_painting_by_id(userId)
            if not admin
            else database.get_paintings()
        )
        headers = (
            ["id", "name", "category", "image", "likes"]
            if not admin
            else [
                "id",
                "name",
                "owner",
                "category",
                "created",
                "image",
                "phone",
                "likes",
            ]
        )
        return jsonify({"success": True, "data": convertToObject(headers, painters)})
    except Exception as error:
        return abort(jsonify({"success": False}))


@painting.route("/get_user_paintings/<id>", methods=["GET", "POST"])
def get_user_paintings(id):
    custom_login_required()
    try:
        painters = database.get_painting_by_id(id)
        headers = ["id", "name", "category", "image", "likes"]
        response = jsonify(
            {"success": True, "data": convertToObject(headers, painters)}
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
