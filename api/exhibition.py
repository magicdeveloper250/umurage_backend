from psycopg2 import IntegrityError, DatabaseError, OperationalError
from flask import Blueprint, request, jsonify
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
            None,
            request.form.get("description"),
        )
        new_item = exhibition.add_exhibition()
        return jsonify({"success": True, "data": new_item}), 201
    except IntegrityError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Exhibition already exists"}), 409
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Exhibition already exists"}), 409
    except (DatabaseError, OperationalError):
        return jsonify(
            {"success": False, "message": "Data submitted has an error, try again"}, 400
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
        return jsonify({"success": False, "message": "Connection error"}), 500

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error, try again"}), 500


@exhibition.route("/get_exhibition/<id>", methods=["GET"])
def get_exhibition(id):
    """ROUTE FOR GETTING EXHIBITIONS BY ID"""
    try:
        return jsonify(Exhibition.get_exhibition(id)), 200
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/get_all_exhibitions", methods=["GET"])
@admin_required
def get_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return jsonify({"success": True, "data": Exhibition.get_exhibitions()}), 200
    except Exception as error:
        current_app.logger.error(str(error))
        return (
            jsonify(
                {
                    "success": True,
                    "message": "unknown error",
                }
            ),
            500,
        )


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_active_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:

        return (
            jsonify({"success": True, "data": Exhibition.get_active_exhibitions()}),
            200,
        )
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([]), 500


@exhibition.route("/get_pending_exhibitions", methods=["GET"])
def get_pending_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return (
            jsonify({"success": True, "data": Exhibition.get_pending_exhibitions()}),
            200,
        )
    except Exception as error:
        current_app.logger.error(str(error))
        return (
            jsonify(
                {
                    "success": True,
                    "message": "unknown error",
                }
            ),
            500,
        )


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
        return jsonify({"success": False, "message": "Connection error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error"}), 500


@exhibition.route("/update_exhibition/<id>", methods=["PUT"])
@admin_required
def update_exhibition(id):
    try:
        exhibition_banner_file = request.files.get("banner")
        exhbition_banner_str = request.form.get("banner")
        image_url = None
        new_banner = False

        # check if new exhibition banner uploaded or the existing one is stil available
        if exhibition_banner_file:
            new_banner = True
        elif exhbition_banner_str:
            new_banner = False

        if new_banner:
            image_url = filemanager.save_exhibition_banner_file(
                exhibition_banner_file, request.form.get("host")
            )
        else:
            image_url = exhbition_banner_str

        exhibition = Exhibition(
            str(id),
            request.form.get("name"),
            request.form.get("start_date"),
            request.form.get("end_date"),
            request.form.get("host"),
            request.form.get("entrace_fees"),
            image_url,
            request.form.get("status"),
            request.form.get("description"),
        )
        exhibition.update_exhibition()
        updated_exhibition = {
            "id": id,
            "description": request.form.get("description"),
            "enddate": request.form.get("end_date"),
            "fees": [request.form.get("entrace_fees")],
            "host": request.form.get("host"),
            "image": image_url,
            "name": request.form.get("name"),
            "startdate": request.form.get("start_date"),
            "status": request.form.get("status"),
        }
        return jsonify({"success": True, "data": updated_exhibition}), 200
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "exhibitionExist": True}), 409
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error"}), 500


@exhibition.route("/change_exhibition_status", methods=["PUT"])
@admin_required
def change_exhibition_status():
    try:
        id = request.form.get("id")
        current_status = request.form.get("current_status")
        new_status = "active" if current_status == "pending" else "pending"
        updated_exhibition = Exhibition.change_exhibition_status(id, new_status)
        return jsonify({"success": True, "data": updated_exhibition}), 201

    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "file already exists"}), 409
    except Exception as error:
        current_app.logger.error(str(error))
        return (
            jsonify(
                {
                    "success": False,
                    "message": "unknown error",
                }
            ),
            500,
        )
