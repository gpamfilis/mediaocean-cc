import logging
import logging.config as logconf
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.bizlogic.errors import EnvironmentVariableError, init_errors
from app.bizlogic.post import fetch_and_save_posts  # Adjust import path as needed
from app.database.engine import init_db

load_dotenv(override=True)

cors = CORS(resources={r"/api/*": {"origins": "*"}})

logconf.fileConfig(fname="logger.conf", disable_existing_loggers=False)


logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    cors.init_app(app)

    init_errors(app)

    db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

    if not db_uri:
        raise EnvironmentVariableError("SQLALCHEMY_DATABASE_URI not defined")

    init_db(db_uri)

    fetch_and_save_posts()

    from app.api.v1 import api as api_v1_blueprint

    app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

    @app.route("/")
    def health():
        return "Alive and Thursty for Vengeance"

    return app
