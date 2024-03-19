from . import EMAIL_KEY
from flask import request, render_template, current_app
import db.painter as database
from flask import Blueprint
import jwt
from flask import jsonify

verify = Blueprint(name="verify", import_name="verify")


@verify.route("/verify", methods=["POST"])
def verify_email():
    """ROUTE FOR EMAIL VERIFICATION"""
    token = request.form.get("token")
    try:
        payload = dict(jwt.decode(token, EMAIL_KEY, algorithms=["HS256"]))
        id = payload.get("id")
        email = payload.get("email")
        database.verify_email(id, email)
        return jsonify({"success": True})
    except Exception as error:
        current_app.logger.error(str(error))
        return jsonify({"success": False})
