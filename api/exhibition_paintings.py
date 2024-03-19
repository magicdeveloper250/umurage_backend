from psycopg2.errors import DatabaseError, OperationalError
from auth.UserAuth import admin_required, payment_required
from flask import Blueprint, request, jsonify
from helperfunctions import convertToObject
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
        return jsonify({"success": resp})
    except (DatabaseError, OperationalError):
        return jsonify(
            {
                "success": False,
                "message": "The information submitted has an error, please check",
            }
        )

    except (
        ConnectionError,
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
    ):
        return jsonify({"success": False, "message": "connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error try again"})


@exhibition_paintings.route("/get_exhibition_paintings/<id>", methods=["GET"])
@payment_required
def get_exhibition_painting(id):
    """ROUTE FOR GETTING EXHIBITION PAINTING"""
    try:
        paintings = ExhibitionPainting.get_exhibition_painting(id)
        return jsonify(paintings)
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify([])
