import logging

from flask import request

from app.api.responses import standard_response
from app.bizlogic.anomaly import get_anomaly_objects
from app.database.engine import DBsession

from . import api

logger = logging.getLogger(__name__)


@api.route("/anomalies", methods=["GET"])
def get_anomalies():
    logger.info("Fetching Anomalies")
    session = DBsession()

    # Get parameters from request
    character_limit = request.args.get(
        "anomalies_character_limit", default=15, type=int
    )
    similarity_threshold = request.args.get(
        "post_similarity_threshold", default=50, type=int
    )
    min_posts = request.args.get("min_posts", default=5, type=int)

    sort_by = request.args.get("sort_by", default="user_id")
    sort_order = request.args.get("sort_order", default="asc")

    # Get all anomalies
    anomalies = get_anomaly_objects(
        session=session,
        similarity_threshold=similarity_threshold,
        min_posts=min_posts,
        character_limit=character_limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = {"anomalies": anomalies}

    session.close()

    return standard_response(data=response)
