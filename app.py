from flask import Flask, make_response, jsonify, request
from api.painter import painter
from api.painting import painting
from api.blog import blog
from api.exhibition import exhibition
from api.exhibition_paintings import exhibition_paintings
from auth.UserAuth import auth
from auth.verify import verify
from payment.paypal import payment
from api.mtn import mtn
from flask_cors import CORS
from auth.UserAuth import auth, loginmanager
from api.customer import customer
import logging


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
app.register_blueprint(customer)
app.register_blueprint(verify)
app.register_blueprint(mtn)

log_level = logging.DEBUG
log_file = "umurage.log"
log_mode = "a"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=log_level, filename=log_file, format=log_format)


CORS(
    app,
    origins=[
        "https://umuragearthubf.onrender.com",
        "http://localhost:5173",
        "https://umuragearts.com",
    ],
)
loginmanager.init_app(app)
