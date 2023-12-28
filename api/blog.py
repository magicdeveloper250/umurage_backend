from flask import Blueprint, request, jsonify
import db.blog as database
from helperfunctions import convertToObject

blog = Blueprint(name="blog", import_name="blog")


@blog.route("/api/blog/add_new_blog", methods=["PUT"])
def post_blog():
    blog = request.get_json()
    database.add_new_blog(blog)
    return jsonify({"success": True})


@blog.route("/api/blog/get_blogs", methods=["GET"])
def get_blogs():
    blogs = database.get_blogs()
    headers = ["Id", "Title", "Content", "Created", "Author"]
    return jsonify(convertToObject(headers, blogs))


@blog.route("/api/blog/delete_blog/<id>", methods=["DELETE"])
def delete_blog(id):
    database.delete_blog(id)
    return jsonify({"success": True})
