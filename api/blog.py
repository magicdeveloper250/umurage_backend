from auth.UserAuth import admin_required
from helperfunctions import convertToObject
import db.blog as database
from flask import Blueprint, request, jsonify


blog = Blueprint(name="blog", import_name="blog")
HEADERS = ["id", "title", "content", "created", "author"]


@blog.route("/blog/add_new_blog", methods=["POST"])
@admin_required
def post_blog():
    global HEADERS
    blog = dict(request.form)
    added_post = database.add_blog(blog)
    return jsonify({"success": True, "data": convertToObject(HEADERS, added_post)})


@blog.route("/blog/get_blogs", methods=["GET"])
def get_blogs():
    global HEADERS
    blogs = database.get_blogs()
    return jsonify(convertToObject(HEADERS, blogs))


@blog.route("/blog/get_blogs/<id>")
def get_blog_by_id(id):
    blogs = database.get_blogs(id)
    return jsonify(convertToObject(HEADERS, blogs))


@blog.route("/blog/delete_blog/<id>", methods=["DELETE"])
@admin_required
def delete_blog(id):
    global HEADERS
    deleted_blog = database.delete_blog(id)
    return jsonify({"success": True, "data": convertToObject(HEADERS, deleted_blog)})
