from flask import Blueprint
import jwt
import db.painter as database
from . import EMAIL_KEY, AFTER_EMAIL_VERIFICATION_REDIRECT
from flask import request, render_template, current_app

verify = Blueprint(name="verify", import_name="verify")


@verify.route("/verify", methods=["GET"])
def verify_email():
    token = request.args.get("token")

    try:
        payload = dict(jwt.decode(token, EMAIL_KEY, algorithms=["HS256"]))
        id = payload.get("id")
        email = payload.get("email")
        database.verify_email(id, email)
        return render_template(
            "email_verified.html", redirect_url=AFTER_EMAIL_VERIFICATION_REDIRECT
        )
    except Exception as error:
        current_app.logger.error(str(error))
        return render_template("email_not_verified.html")
