from psycopg2.errors import DatabaseError, OperationalError
from auth.UserAuth import admin_required, payment_required
from flask import Blueprint, request, jsonify
from models.exhibitionPainting import ExhibitionPainting
from filemanagement import filemanager
from flask import current_app

exhibition_paintings = Blueprint(
    name="exhibition_paintings", import_name="exhibition_paintings"
)
HEADERS = ("id", "name", "description", "image", "audio", "owner", "painter")


@exhibition_paintings.route("/add_exhibition_painting", methods=["POST"])
@admin_required
def add_painting():
    """ROUTE FOR ADDING NEW EXHIBITION PAINTING"""
    try:
        image_url, audio_url = filemanager.add_painting_file(
            request.form.get("owner"),
            image=request.files.get("image"),
            audio=request.files.get("audio"),
        )
        painting = ExhibitionPainting(
            None,
            request.form.get("name"),
            request.form.get("description"),
            image_url,
            audio_url,
            request.form.get("ex"),
            request.form.get("owner"),
        )
        resp = painting.add_exhibition_painting()
        return jsonify({"success": resp}), 201
    except (DatabaseError, OperationalError):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "The information submitted has an error, please check",
                }
            ),
            400,
        )

    except (
        ConnectionError,
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
    ):
        return jsonify({"success": False, "message": "connection error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error"}), 500


@exhibition_paintings.route("/get_exhibition_paintings/<id>", methods=["GET"])
@payment_required
def get_exhibition_painting(id):
    """ROUTE FOR GETTING EXHIBITION PAINTING"""
    try:
        paintings = ExhibitionPainting.get_exhibition_painting(id)
        return jsonify({"success": True, "data": paintings}), 200

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error"}), 500


@exhibition_paintings.route("/get_all_exhibition_paintings", methods=["GET"])
@admin_required
def get_exhibition_all_paintings():
    """ROUTE FOR GETTING EXHIBITION PAINTING"""
    try:
        paintings = ExhibitionPainting.get_all_paintings()
        return jsonify({"success": True, "data": paintings}), 200

    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "unknown error"}), 500


@exhibition_paintings.route("/delete_exhibition_painting/<id>", methods=["DELETE"])
@admin_required
def delete_exhibition_painting(id):
    """ROUTE FOR GETTING EXHIBITION PAINTING"""
    try:
        painting_deleted = ExhibitionPainting.delete_exhibition_painting(id)
        if painting_deleted:
            return (
                jsonify(
                    {
                        "success": painting_deleted,
                    }
                ),
                204,
            )

        return jsonify({"success": False, "message": "unknown error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Unknown error"}), 500
