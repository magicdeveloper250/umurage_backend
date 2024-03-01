from auth.UserAuth import admin_required, payment_required, image_protected
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from flask import current_app
from helperfunctions import convertToObject
import db.exhibition_paintings as database
import requests


exhibition_paintings = Blueprint(
    name="exhibition_paintings", import_name="exhibition_paintings"
)
HEADERS = ("id", "name", "description", "image", "audio", "owner", "painter")


@exhibition_paintings.route("/add_exhibition_painting", methods=["POST"])
@admin_required
def add_painting():
    try:
        painting = {}
        painting["name"] = request.form.get("name")
        painting["description"] = request.form.get("description")
        painting["painter"] = request.form.get("owner")
        image = request.files.get("image")
        audio = request.files.get("audio")

        image_url, audio_url = filemanager.add_painting_file(
            request.form.get("owner"), image=image, audio=audio
        )
        painting["image"] = image_url

        painting["audio"] = audio_url
        painting["owner"] = request.form.get("ex")
        database.add_exhibition_paintings(painting)

        return jsonify({"success": True})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})


@exhibition_paintings.route("/get_exhibition_paintings/<id>", methods=["GET"])
@payment_required
def get_exhibition_painting(id):
    global HEADERS
    try:
        paintings = database.get_exhibition_painting(id)
        return jsonify(convertToObject(HEADERS, paintings))
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


# @exhibition_paintings.route("/exhibition_painting", methods=["GET"])
# # @image_protected
# def get_painting_file():
#     encrypted_path = request.args.get("f")
#     path = filemanager.get_exhibition_painting_file(encrypted_path)
#     file = requests.get(path)
#     print(path)
#     return send_file(file.content)
