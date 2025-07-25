import logging
from typing import List

from app.api.responses import standard_response
from app.database.engine import DBsession
from app.database.models import User

from . import api

logger = logging.getLogger(__name__)


@api.route("/users", methods=["DELETE"])
def delete_all_posts():
    session = DBsession()
    post_objs: List[User] = session.query(User).all()
    for post in post_objs:
        session.delete(post)
    session.commit()
    session.close()

    return standard_response(status_code=204)
