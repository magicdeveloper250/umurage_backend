from auth import SESSION_KEY
from auth.UserAuth import custom_login_required, user_or_admin_required
import cryptocode
from filemanagement import filemanager
from flask import Blueprint, request, abort, jsonify, send_file
from flask import current_app
from helperfunctions import convertToObject
import db.painting as database


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
@custom_login_required
def add_new_painting():
    global HEADERS
    try:
        new_painting = {}
        new_painting["name"] = request.form.get("name")
        new_painting["category"] = request.form.get("category")
        new_painting["owner"] = cryptocode.decrypt(
            request.form.get("owner"), SESSION_KEY
        )
        new_painting["created"] = request.form.get("created")
        image_file = request.files.get("painting")

        # uploading image to cloudinary
        image_url = filemanager.add_user_painting_file(
            image_file, new_painting["owner"]
        )
        new_painting["image"] = image_url
        added_painting = database.add_new_painting(new_painting)

        return jsonify(
            {"success": True, "data": convertToObject(HEADERS, added_painting)}
        )
    except Exception as error:
        current_app.logger.error(str(error))
        return abort(jsonify({"success": False, "erro": str(error)}))


@painting.route("/get_paintings", methods=["GET", "POST"])
def get_paintings():
    global HEADERS
    try:
        painters = database.get_paintings()
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        current_app.logger.error(str(error))
        return abort(jsonify({"success": False, "data": []}))


@painting.route("/uploads/paintings/<filename>")
def send_painting_file(filename):
    path = filemanager.get_user_painting_file_path(filename)
    return send_file(path)


@painting.route("/delete_painting/<id>", methods=["DELETE"])
def delete_painting(id):
    global HEADERS
    user, admin = user_or_admin_required()
    userId = cryptocode.decrypt(request.headers.get("userId"), SESSION_KEY)
    try:
        deleted_painting = database.delete_painting(id, userId)
        # filemanager.delete_user_painting_file(deleted_painting[0][5])
        painters = (
            database.get_painting_by_id(userId)
            if not admin
            else database.get_paintings()
        )
        HEADERS = MIN_HEADER if not admin else HEADERS
        return jsonify({"success": True, "data": convertToObject(HEADERS, painters)})
    except Exception as error:
        current_app.logger.error(str(error))
        return abort(jsonify({"success": False}))


@painting.route("/get_user_paintings", methods=["GET", "POST"])
@custom_login_required
def get_user_paintings():
    global MIN_HEADER
    userId = cryptocode.decrypt(request.form.get("userId"), SESSION_KEY)
    try:
        painters = database.get_painting_by_id(userId)
        response = jsonify(
            {"success": True, "data": convertToObject(MIN_HEADER, painters)}
        )
        return response
    except Exception as error:
        current_app.logger.error(error)
        return abort(jsonify({"success": False}))


@painting.route("/like/<painting_id>", methods=["POST"])
def like(painting_id):
    try:
        liked = database.like(painting_id)
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
        current_app.logger.error(str(error))
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
        current_app.logger.error(str(error))
        return jsonify({"success": False, "error": error})
