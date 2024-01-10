from flask import Blueprint, request, jsonify, send_file
from helperfunctions import convertToObject, generate_mime
from werkzeug.utils import secure_filename
import os
import db.exhibition_paintings as database
from auth.UserAuth import admin_required, payment_required, image_protected

exhibition_paintings = Blueprint(
    name="exhibition_paintings", import_name="exhibition_paintings"
)


@exhibition_paintings.route("/add_exhibition_painting", methods=["POST"])
def add_painting():
    admin_required()
    painting = {}
    painting["name"] = request.form.get("name")
    painting["description"] = request.form.get("description")
    painting["painter"] = request.form.get("painter")
    image = request.files.get("image")
    audio = request.files.get("audio")
    # customize file names
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
        + f"/images/exhibition_paintings/{request.form.get('owner')}/"
        + i_name
    )
    audio_name = (
        request.base_url.replace("/add_exhibition_painting", "")
        + f"/images/exhibition_paintings/{request.form.get('owner')}/"
        + a_name
    )
    painting["image"] = name
    painting["audio"] = audio_name
    painting["owner"] = request.form.get("owner")
    database.add_exhibition_paintings(painting)

    # save file to file system
    image.save(
        os.path.join(
            os.getcwd() + f"/images/exhibition_paintings/{request.form.get('owner')}",
            i_name,
        )
    )
    audio.save(
        os.path.join(
            os.getcwd() + f"/images/exhibition_paintings/{request.form.get('owner')}",
            a_name,
        )
    )
    return jsonify({"success": True})


@exhibition_paintings.route("/get_exhibition_paintings/<id>", methods=["GET"])
def get_exhibition_painting(id):
    payment_required()
    paintings = database.get_exhibition_painting(id)
    headers = ("id", "name", "description", "image", "audio", "owner", "painter")
    return jsonify(convertToObject(headers, paintings))


@exhibition_paintings.route(
    "/images/exhibition_paintings/<exhibition_id>/<filename>", methods=["GET"]
)
def get_painting_file(exhibition_id, filename):
    image_protected()
    fName, extension = os.path.splitext(
        os.getcwd() + f"images/{exhibition_id}/{filename}"
    )
    mime = generate_mime(extension)
    response = send_file(
        os.path.join(
            os.getcwd() + f"/images/exhibition_paintings",
            secure_filename(f"{exhibition_id}") + "/" + secure_filename(f"{filename}"),
        ),
        mimetype=mime if mime else "",
    )
    return response
