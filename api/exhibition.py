from psycopg2 import IntegrityError, DatabaseError, OperationalError
from flask import Blueprint, request, jsonify, send_file
from auth.UserAuth import admin_required
from models.exhibition import Exhibition
from filemanagement import filemanager
from urllib3.exceptions import (
    HTTPError,
    HTTPWarning,
    RequestError,
    ResponseError,
    NewConnectionError,
)
from flask import current_app

exhibition = Blueprint(name="exhibition", import_name="exhibition")


@exhibition.route("/add_new_exhibition", methods=["PUT"])
@admin_required
def add_exhibition():
    """ROUTE FOR ADDING NEW EXHIBITION"""
    try:
        exhibition_banner_file = request.files.get("banner")

        image_url = filemanager.save_exhibition_banner_file(
            exhibition_banner_file, request.form.get("host")
        )
        exhibition = Exhibition(
            None,
            request.form.get("name"),
            request.form.get("start_date"),
            request.form.get("end_date"),
            request.form.get("host"),
            request.form.get("entrace_fees"),
            image_url,
        )
        new_item = exhibition.add_exhibition()
        return jsonify({"success": True, "data": new_item})
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "messag": "Exhibition already exists"})
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Exhibition already exists"})
    except (DatabaseError, OperationalError):
        return jsonify(
            {"success": False, "message": "Data submitted has an error, try again"}
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        NewConnectionError,
        ConnectionError,
        ResponseError,
        RequestError,
        HTTPWarning,
        HTTPError,
    ):
        return jsonify({"success": False, "message": "Connection error"})

    except Exception as error:
        current_app.logger.error(str(error))
        print(str(error))
        return jsonify({"success": False, "message": "uncaught error, try again"})


@exhibition.route("/get_exhibition/<id>", methods=["GET"])
def get_exhibition(id):
    """ROUTE FOR GETTING EXHIBITIONS BY ID"""
    try:
        return jsonify(Exhibition.get_exhibition(id))
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return jsonify(Exhibition.get_exhibitions())
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/delete_exhibition/<id>/<name>", methods=["DELETE"])
@admin_required
def delete_exhibition(id, name):
    """ROUTE FOR DELETING EXHIBITION"""
    try:
        return jsonify({"success": True, "data": Exhibition.delete_exhibition(id)})
    except (DatabaseError, OperationalError) as error:
        return jsonify({"success": False, "message": str(error)})
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@exhibition.route("/update_exhibition/<id>/<name>", methods=["PUT"])
@admin_required
def update_exhibition(id, name):
    try:
        exhibition_banner_file = request.files.get("banner")

        image_url = filemanager.save_exhibition_banner_file(
            exhibition_banner_file, request.form.get("host")
        )
        exhibition = Exhibition(
            request.form.get("name"),
            request.form.get("start_date"),
            request.form.get("end_date"),
            request.form.get("host"),
            request.form.get("entrace_fees"),
            image_url,
        )
        exhibition.add_exhibition()
        return jsonify({"success": True})
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"exhibitionExist": True})
