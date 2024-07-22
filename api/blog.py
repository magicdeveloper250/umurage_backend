from psycopg2.errors import DatabaseError, OperationalError
from flask import Blueprint, request, jsonify
from auth.UserAuth import admin_required
from flask import current_app
from models.blog import Blog

blog = Blueprint(name="blog", import_name="blog")
HEADERS = ["id", "title", "content", "created", "author"]


@blog.route("/blog/add_new_blog", methods=["POST"])
@admin_required
def post_blog():
    """ROUTE FOR ADDING NEW BLOG"""
    blog = Blog(
        None,
        request.form.get("title"),
        request.form.get("content"),
        request.form.get("created"),
        request.form.get("author"),
    )
    added_post = blog.add_blog()
    return jsonify({"success": True, "data": added_post}), 201


@blog.route("/blog/get_blogs", methods=["GET"])
def get_blogs():
    """ROUTE FOR GETTING ALL BLOGS"""
    blogs = Blog.get_blogs()
    return jsonify({"success": True, "data": blogs}), 200


@blog.route("/blog/get_blogs/<id>")
def get_blog_by_id(id):
    """ROUTE FOR GETTING BLOG BY ID"""
    try:
        blogs = Blog.get_blogs(id=id)
        return jsonify({"success": True, "data": blogs}), 200
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


@blog.route("/blog/delete_blog/<id>", methods=["DELETE"])
@admin_required
def delete_blog(id):
    """ROUTE FOR DELETING BLOG"""
    try:
        deleted_blog = Blog.delete_blog(id)
        return jsonify({"success": True, "data": [deleted_blog]})
    except (DatabaseError, OperationalError) as database_error:
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(database_error),
                }
            ),
            204,
        )
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
