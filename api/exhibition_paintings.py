from auth.UserAuth import admin_required, payment_required, image_protected
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from helperfunctions import convertToObject, generate_mime
from werkzeug.utils import secure_filename
import db.exhibition_paintings as database

exhibition_paintings = Blueprint(
    name="exhibition_paintings", import_name="exhibition_paintings"
)
HEADERS = ("id", "name", "description", "image", "audio", "owner", "painter")


@exhibition_paintings.route("/add_exhibition_painting", methods=["POST"])
def add_painting():
    admin_required()
    painting = {}
    painting["name"] = request.form.get("name")
    painting["description"] = request.form.get("description")
    painting["painter"] = request.form.get("painter")
    image = request.files.get("image")
    audio = request.files.get("audio")
    i_name = secure_filename(
        request.form.get("owner")
        + "_"
        + request.form.get("name")
        + "_"
        + image.filename
    )
    a_name = secure_filename(
        request.form.get("owner") + request.form.get("name") + audio.filename
    )
    name = (
        request.base_url.replace("/add_exhibition_painting", "")
        + f"/uploads/exhibition_paintings/{request.form.get('owner')}/"
        + i_name
    )
    audio_name = (
        request.base_url.replace("/add_exhibition_painting", "")
        + f"/uploads/exhibition_paintings/{request.form.get('owner')}/"
        + a_name
    )
    painting["image"] = name
    painting["audio"] = audio_name
    painting["owner"] = request.form.get("owner")
    database.add_exhibition_paintings(painting)
    filemanager.add_painting_file(
        request.form.get("owner"),
        image={"file": image, "filename": i_name},
        audio={"file": audio, "filename": a_name},
    )

    return jsonify({"success": True})


@exhibition_paintings.route("/get_exhibition_paintings/<id>", methods=["GET"])
def get_exhibition_painting(id):
    global HEADERS
    payment_required()
    paintings = database.get_exhibition_painting(id)
    return jsonify(convertToObject(HEADERS, paintings))


@exhibition_paintings.route(
    "/uploads/exhibition_paintings/<exhibition_id>/<filename>", methods=["GET"]
)
def get_painting_file(exhibition_id, filename):
    image_protected()
    path = filemanager.get_painting_file_path(exhibition_id, filename)
    return send_file(path)
