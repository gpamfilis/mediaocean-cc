import logging

from flask import request

from app.api.responses import standard_response
from app.bizlogic.summary import (
    count_all_users_words_from_titles,
    identify_users_with_most_unique_titles_detailed,
)
from app.database.engine import DBsession

from . import api

logger = logging.getLogger(__name__)


@api.route("/summary", methods=["GET"])
def route_get_full_summary():
    session = DBsession()
    number_of_users = request.args.get("max_number_of_users", default=4, type=int)
    number_of_words = request.args.get("limit_words", default=10, type=int)

    response = identify_users_with_most_unique_titles_detailed(
        max_number_of_users=number_of_users, session=session
    )
    response["most_frequent_words"] = count_all_users_words_from_titles(
        session=session, limit=number_of_words
    )
    session.close()

    return standard_response(data=response)
