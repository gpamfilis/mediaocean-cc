from flask import Blueprint

api = Blueprint("apiv1", "__name__")

from . import anomaly, post, summary  # noqa
