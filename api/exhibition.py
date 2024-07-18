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
            None,
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


@exhibition.route("/get_all_exhibitions", methods=["GET"])
@admin_required
def get_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return jsonify({"success": True, "data": Exhibition.get_exhibitions()})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify(
            {
                "success": True,
                "message": "unable to find what you are looking for try again",
            }
        )


@exhibition.route("/get_exhibitions", methods=["GET"])
def get_active_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return jsonify({"success": True, "data": Exhibition.get_active_exhibitions()})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])


@exhibition.route("/get_pending_exhibitions", methods=["GET"])
def get_pending_exhibitions():
    """ROUTE FOR GETTING ALL EXHIBITIONS"""
    try:
        return jsonify({"success": True, "data": Exhibition.get_pending_exhibitions()})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify(
            {
                "success": True,
                "message": "unable to find what you are looking for try again",
            }
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


@exhibition.route("/change_exhibition_status", methods=["PUT"])
@admin_required
def change_exhibition_status():
    try:
        id = request.form.get("id")
        current_status = request.form.get("current_status")
        new_status = "active" if current_status == "pending" else "pending"
        updated_exhibition = Exhibition.change_exhibition_status(id, new_status)
        if update_exhibition:
            return jsonify({"success": True, "data": updated_exhibition})
        else:
            return jsonify(
                {
                    "success": False,
                    "message": "unable to update exhibition right now. try again later",
                }
            )
    except FileExistsError as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "there is some duplication"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify(
            {
                "success": False,
                "message": "unable to update exhibition right now. try again later",
            }
        )
