from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from api.painter import painter
from api.painting import painting
from api.blog import blog
from api.exhibition import exhibition
from api.exhibition_paintings import exhibition_paintings
from api.comment import comment
from auth.UserAuth import auth
from auth.verify import verify
from payment.paypal import payment
from api.mtn import mtn
from flask_cors import CORS
from auth.UserAuth import auth
from api.customer import customer
import logging
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
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
app.register_blueprint(comment)

log_level = logging.DEBUG
log_file = "umurage.log"
log_mode = "a"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=log_level, filename=log_file, format=log_format)
CORS(
    app,
    supports_credentials=True,
    resources={
        # r"/*": {"origins": [os.environ.get("FRONT_END_SERVER"), "http://localhost"]}
        r"/*": {"origins": "*"}
    },
)
