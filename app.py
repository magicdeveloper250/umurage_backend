from flask import Flask, make_response, jsonify, request
from api.painter import painter
from api.painting import painting
from api.blog import blog
from api.exhibition import exhibition
from api.exhibition_paintings import exhibition_paintings

from auth.UserAuth import auth
import db.painter as database
from db import painter as database
from api.payment import payment
from flask import make_response
import cryptocode
from auth.user import User
from flask_cors import CORS
from flask import redirect
from flask_login import LoginManager, login_required, login_user, logout_user, utils
from auth.UserAuth import auth, loginmanager
import click

SECRET_KEY = "4bbb5d19-4dee-40d8-a2d8-1b75da3e9d01"
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(painter)
app.register_blueprint(painting)
app.register_blueprint(blog)
app.register_blueprint(exhibition)
app.register_blueprint(exhibition_paintings)
app.register_blueprint(auth)
app.register_blueprint(payment)
CORS(
    app,
    origins=["https://umuragearthubf.onrender.com"],
)
loginmanager.init_app(app)
