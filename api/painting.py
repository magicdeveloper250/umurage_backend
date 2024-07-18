from auth.UserAuth import custom_login_required, user_or_admin_required
from flask import Blueprint, request, abort, jsonify, send_file
from psycopg2.errors import DatabaseError, OperationalError
from helperfunctions import convertToObject
from filemanagement import filemanager
from models.painting import Painting
from flask import current_app
from auth import SESSION_KEY
import cryptocode

painting = Blueprint(name="painting", import_name="painting")

HEADERS = [
    "id",
    "name",
    "owner",
    "category",
    "created",
    "image",
    "phone",
    "likes",
]
MIN_HEADER = ["id", "name", "category", "image", "likes"]


@painting.route("/add_new_painting", methods=["PUT"])
@custom_login_required
def add_new_painting():
    """ROUTE FOR ADDING NEW PAINTING"""
    global HEADERS
    try:
        painting_owner = cryptocode.decrypt(request.form.get("owner"), SESSION_KEY)
        image_file = request.files.get("painting")
        image_url = filemanager.add_user_painting_file(image_file, painting_owner)
        painting = Painting(
            request.form.get("name"),
            request.form.get("category"),
            painting_owner,
            request.form.get("created"),
            image_url,
        )
        added_painting = painting.add_painting()
        return jsonify(
            {
                "success": True,
                "data": convertToObject(["id", "image", "likes"], added_painting),
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ) as error:
        current_app.logger.error(str(error))
        return abort(
            jsonify(
                {
                    "success": False,
                    "message": "Connection error",
                }
            )
        )
    except (DatabaseError, OperationalError) as error:
        current_app.logger.error(str(error))
        return abort(
            jsonify(
                {
                    "success": False,
                    "message": "Some data submitted has an error, try again",
                }
            )
        )

    except Exception as error:
        current_app.logger.error(str(error))
        return abort(
            jsonify({"success": False, "message": "uncaught error, try again"})
        )


@painting.route("/get_paintings", methods=["GET", "POST"])
def get_paintings():
    """ROUTE FOR GETTING PAINTINGS"""
    global HEADERS
    try:
        return jsonify(
            {
                "success": True,
                "data": convertToObject(HEADERS, Painting.get_paintings()),
            }
        )
    except Exception as error:
        current_app.logger.error(str(error))
        print(error)
        return abort(jsonify({"success": str(error), "data": []}))


@painting.route("/delete_painting/<painting_id>", methods=["DELETE"])
def delete_painting(painting_id):
    global HEADERS
    user, admin = user_or_admin_required()
    userId = cryptocode.decrypt(request.headers.get("userId"), SESSION_KEY)
    try:
        Painting.delete_painting(painting_id)
        paintings = (
            Painting.get_user_paintings(userId)
            if not admin
            else Painting.get_paintings()
        )
        header = MIN_HEADER if not admin else HEADERS
        return jsonify({"success": True, "data": convertToObject(header, paintings)})
    except (DatabaseError, OperationalError):
        return jsonify(
            {"success": False, "message": "Data submitted has an error, try again"}
        )
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


@painting.route("/get_user_paintings", methods=["GET", "POST"])
@custom_login_required
def get_user_paintings():
    """ROUTE FOR GETTING USER PAINTINGS"""
    global MIN_HEADER
    userId = cryptocode.decrypt(request.form.get("userId"), SESSION_KEY)
    try:
        response = jsonify(
            {
                "success": True,
                "data": convertToObject(
                    MIN_HEADER, Painting.get_user_paintings(userId)
                ),
            }
        )
        return response
    except (DatabaseError, OperationalError) as error:
        current_app.logger.error(str(error))
        return jsonify(
            {
                "success": False,
                "message": "information submitted to the server has error. Please check your info",
            }
        )
    except (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError,
        ConnectionError,
    ) as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "Connection error"})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"})


@painting.route("/like/<painting_id>", methods=["POST"])
def like(painting_id):
    """ROUTE FOR LIKING PAINTING"""
    try:
        liked = Painting.like(painting_id)
        if liked:
            likes = Painting.get_likes(painting_id)
            return jsonify({"success": True, "likes": likes[0]})
        else:
            return jsonify(
                {
                    "success": False,
                }
            )
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


@painting.route("/dislike/<painting_id>", methods=["POST"])
def dislike(painting_id):
    """ROUTE FOR DISLIKE PAINITNG"""
    try:
        liked = Painting.dislike(painting_id)
        if liked:
            likes = Painting.get_likes(painting_id)
            return jsonify({"success": True, "likes": likes[0]})
        else:
            return jsonify(
                {
                    "success": False,
                }
            )
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
