from auth.UserAuth import admin_required
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from flask import current_app
from helperfunctions import convertToObject
from psycopg2 import IntegrityError
from werkzeug.utils import secure_filename
import db.exhibition as database


exhibition = Blueprint(name="exhibition", import_name="exhibition")
HEADERS = ["id", "name", "startdate", "enddate", "host", "fees", "image"]


@exhibition.route("/add_new_exhibition", methods=["PUT"])
@admin_required
def add_exhibition():
    global HEADERS
    try:
        exhibition = {}
        exhibition["name"] = request.form.get("name")
        exhibition["start_date"] = request.form.get("start_date")
        exhibition["end_date"] = request.form.get("end_date")
        exhibition["host"] = request.form.get("host")
        exhibition["entrace_fees"] = request.form.get("entrace_fees")
        exhibition_banner_file = request.files.get("banner")

        image_url = filemanager.save_exhibition_banner_file(
            exhibition_banner_file, exhibition["host"]
        )
        exhibition["banner"] = image_url
        new_item = database.add_new_exhibition(exhibition)
        return jsonify({"success": True, "data": convertToObject(HEADERS, new_item)})
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"exhibitionExist": True})
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"exhibitionExist": True})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})


@exhibition.route("/get_exhibition/<id>", methods=["GET"])
def get_exhibition(id):
    global HEADERS
    try:
        exhibition = database.get_exhibition(id)
        return jsonify(convertToObject(HEADERS, exhibition)[0])
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_exhibitions():
    global HEADERS
    try:
        exhibitions = database.get_exhibitions()
        return jsonify(convertToObject(HEADERS, exhibitions))
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/uploads/exhibitions/<filename>")
def send_exhibition_image(filename):
    try:
        file = filemanager.get_exhibition_banner_path(filename)
        return send_file(file)
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify("File not loaded")


@exhibition.route("/delete_exhibition/<id>/<name>", methods=["DELETE"])
@admin_required
def delete_exhibition(id, name):
    global HEADERS
    try:
        deleted_exhibition = database.delete_exhibition(id)
        # filemanager.delete_exhibition_painting_dir(name)
        # filemanager.delete_exhibition_banner_file(deleted_exhibition[0][6])
        return jsonify(
            {"success": True, "data": convertToObject(HEADERS, deleted_exhibition)}
        )
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})


@exhibition.route("/update_exhibition/<id>/<name>", methods=["PUT"])
@admin_required
def update_exhibition(id, name):
    try:
        exhibition = {}
        exhibition["name"] = request.form.get("name")
        exhibition["start_date"] = request.form.get("start_date")
        exhibition["end_date"] = request.form.get("end_date")
        exhibition["host"] = request.form.get("host")
        exhibition["entrace_fees"] = request.form.get("entrace_fees")
        exhibition_banner_file = request.files.get("banner")
        banner_fname = (
            request.base_url.replace(f"/update_exhibition/{id}/{name}/", "")
            + "/uploads/exhibitions/"
            + exhibition_banner_file.filename
        )
        exhibition["banner"] = banner_fname
        database.update_exhibition(exhibition, id)
        filemanager.save_exhibition_banner_file(exhibition_banner_file)
        filemanager.rename_exhibition_folder_name(name, exhibition["name"])
        return jsonify({"success": True})
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"exhibitionExist": True})
