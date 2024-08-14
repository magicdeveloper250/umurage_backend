from psycopg2.errors import DatabaseError, OperationalError
from flask import Blueprint, request, jsonify
from auth.UserAuth import admin_required
from flask import current_app
from models.comment import Comment

comment = Blueprint(name="comment", import_name="comment")
HEADERS = ["id", "ex_id", "cust_id", "text"]


@comment.route("/comment/add_new_comment", methods=["POST"])
@admin_required
def post_comment():
    """ROUTE FOR ADDING NEW COMMENT"""
    data = request.json
    comment = Comment(
        None,
        data.get("ex_id"),
        data.get("cust_id"),
        data.get("text"),
    )
    new_comment = comment.add_comment()
    return jsonify({"success": True, "data": new_comment}), 201


@comment.route("/comment/get_comments", methods=["GET"])
def get_comments():
    """ROUTE FOR GETTING ALL COMMENT"""
    comments = Comment.get_comments()
    return jsonify({"success": True, "data": comments}), 200


@comment.route("/comment/get_comments/<id>")
def get_comment_by_id(id):
    """ROUTE FOR GETTING BLOG BY ID"""
    try:
        comment = Comment.get_comments(id=id)
        return jsonify({"success": True, "data": comment}), 200
    except (DatabaseError, OperationalError):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "information submitted to the server has error. Please check your info",
                }
            ),
            400,
        )
    except (
        ConnectionRefusedError,
        ConnectionAbortedError,
        ConnectionResetError,
        ConnectionError,
    ):
        return jsonify({"success": False, "message": "Connection error"}), 500
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False, "message": "uncaught error"}), 500


@comment.route("/comment/delete_comment/<id>", methods=["DELETE"])
@admin_required
def delete_comment(id):
    """ROUTE FOR DELETING COMMENT"""
    try:
        deleted_comment = Comment.delete_comment(id)
        return jsonify({"success": True, "data": [deleted_comment]}), 204
    except (DatabaseError, OperationalError) as database_error:
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(database_error),
                }
            ),
        ), 500
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
