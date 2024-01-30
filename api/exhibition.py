from flask import Blueprint, request, jsonify, send_file
import db.exhibition as database
from helperfunctions import convertToObject
from werkzeug.utils import secure_filename
import os
from auth.UserAuth import custom_login_required, admin_required
from flask_login import login_required
from auth.UserAuth import custom_login_required

exhibition = Blueprint(name="exhibition", import_name="exhibition")


def delete_exhibition_file(exhibition_name):
    os.removedirs(
        os.path.join(os.getcwd() + "/images/exhibition_paintings", exhibition_name)
    )


def add_exhibition_folder(name):
    CURRENT_FOLDER = os.getcwd()
    os.chdir(os.getcwd() + "/images/exhibition_paintings")
    os.mkdir(name)
    os.chdir(CURRENT_FOLDER)


def rename_exhibition_folder(old, new):
    CURRENT_FOLDER = os.getcwd()
    os.chdir(os.getcwd() + f"/images/exhibition_paintings")
    os.rename(
        f"{old}",
        f"{new}",
    )

    os.chdir(CURRENT_FOLDER)


@exhibition.route("/add_new_exhibition", methods=["PUT"])
def add_exhibition():
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
            + "/images/exhibitions/"
            + exhibition_banner_file.filename
        )

        exhibition["banner"] = banner_fname

        database.add_new_exhibition(exhibition)
        exhibition_banner_file.save(
            os.path.join(
                os.getcwd() + "/images/exhibitions",
                secure_filename(exhibition_banner_file.filename),
            )
        )
        # creating exhibition folder to be used after while adding paintings
        CURRENT_FOLDER = os.getcwd()
        os.chdir(os.getcwd() + "/images/exhibition_paintings")
        os.mkdir(exhibition["name"])
        os.chdir(CURRENT_FOLDER)

        return jsonify({"success": True})
    except FileExistsError as error:
        return jsonify({"exhibitionExist": True})


@exhibition.route("/get_exhibition/<id>", methods=["GET"])
def get_exhibition(id):
    exhibition = database.get_exhibition(id)

    headers = ["id", "name", "startdate", "enddate", "host", "fees", "image"]
    return jsonify(convertToObject(headers, exhibition)[0])


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_exhibitions():
    exhibitions = database.get_exhibitions()
    headers = ["id", "name", "startdate", "enddate", "host", "fees", "image"]
    return jsonify(convertToObject(headers, exhibitions))


@exhibition.route("/images/exhibitions/<filename>")
def send_exhibition_image(filename):
    fname = secure_filename(filename)
    file = os.path.join(os.getcwd() + "/images/exhibitions", fname)
    return send_file(file)


@exhibition.route("/delete_exhibition/<id>/<name>", methods=["DELETE"])
def delete_exhibition(id, name):
    admin_required()
    try:
        database.delete_exhibition(id)
        exhibitions = database.get_exhibitions()
        headers = ["id", "name", "startdate", "enddate", "host", "fees", "image"]
        delete_exhibition_file(name)
        return jsonify({"success": True, "data": convertToObject(headers, exhibitions)})
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
            + "/images/exhibitions/"
            + exhibition_banner_file.filename
        )

        exhibition["banner"] = banner_fname

        database.update_exhibition(exhibition, id)
        exhibition_banner_file.save(
            os.path.join(
                os.getcwd() + "/images/exhibitions",
                secure_filename(exhibition_banner_file.filename),
            )
        )
        rename_exhibition_folder(name, exhibition["name"])
        return jsonify({"success": True})
    except FileExistsError as error:
        return jsonify({"exhibitionExist": True})
