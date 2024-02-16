from auth.UserAuth import admin_required
from filemanagement import filemanager
from flask import Blueprint, request, jsonify, send_file
from helperfunctions import convertToObject
from psycopg2 import IntegrityError
from werkzeug.utils import secure_filename
import db.exhibition as database


exhibition = Blueprint(name="exhibition", import_name="exhibition")
HEADERS = ["id", "name", "startdate", "enddate", "host", "fees", "image"]


@exhibition.route("/add_new_exhibition", methods=["PUT"])
def add_exhibition():
    global HEADERS
    admin_required()
    try:
        exhibition = {}
        exhibition["name"] = request.form.get("name")
        exhibition["start_date"] = request.form.get("start_date")
        exhibition["end_date"] = request.form.get("end_date")
        exhibition["host"] = request.form.get("host")
        exhibition["entrace_fees"] = request.form.get("entrace_fees")
        exhibition_banner_file = request.files.get("banner")
        banner_fname = (
            request.base_url.replace("/add_new_exhibition", "")
            + "/uploads/exhibitions/"
            + secure_filename(exhibition_banner_file.filename)
        )

        exhibition["banner"] = banner_fname
        new_item = database.add_new_exhibition(exhibition)
        filemanager.save_exhibition_banner_file(exhibition_banner_file)
        filemanager.create_exhibition_painting_dir(exhibition["name"])
        return jsonify({"success": True, "data": convertToObject(HEADERS, new_item)})
    except IntegrityError:
        return jsonify({"exhibitionExist": True})
    except FileExistsError:
        return jsonify({"exhibitionExist": True})
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@exhibition.route("/get_exhibition/<id>", methods=["GET"])
def get_exhibition(id):
    global HEADERS
    exhibition = database.get_exhibition(id)
    return jsonify(convertToObject(HEADERS, exhibition)[0])


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_exhibitions():
    global HEADERS
    exhibitions = database.get_exhibitions()
    return jsonify(convertToObject(HEADERS, exhibitions))


@exhibition.route("/uploads/exhibitions/<filename>")
def send_exhibition_image(filename):
    file = filemanager.get_exhibition_banner_path(filename)
    return send_file(file)


@exhibition.route("/delete_exhibition/<id>/<name>", methods=["DELETE"])
def delete_exhibition(id, name):
    global HEADERS
    admin_required()
    try:
        deleted_exhibition = database.delete_exhibition(id)
        filemanager.delete_exhibition_painting_dir(name)
        filemanager.delete_exhibition_banner_file(deleted_exhibition[0][6])
        return jsonify(
            {"success": True, "data": convertToObject(HEADERS, deleted_exhibition)}
        )
    except Exception as error:
        print(error)
        return jsonify({"success": False})


@exhibition.route("/update_exhibition/<id>/<name>", methods=["PUT"])
def update_exhibition(id, name):
    admin_required()
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
        return jsonify({"exhibitionExist": True})
