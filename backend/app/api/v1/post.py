import logging
from typing import List

from app.api.responses import standard_response
from app.api.schemas import PostSchema
from app.bizlogic.errors import NotFoundError
from app.bizlogic.post import fetch_and_save_posts
from app.database.engine import DBsession
from app.database.models import Post

from . import api

logger = logging.getLogger(__name__)


@api.route("/posts", methods=["GET"])
def list_posts():
    logger.info("Fetching Posts")
    session = DBsession()

    # TODO: fetch messages using worker.
    fetch_and_save_posts()

    post_objs: List[Post] = session.query(Post).all()

    if not post_objs:
        raise NotFoundError("No Posts")

    posts_serialized = PostSchema().dump(post_objs, many=True)

    session.close()

    return standard_response(data=posts_serialized)


@api.route("/posts", methods=["DELETE"])
def delete_all_posts():
    session = DBsession()
    post_objs: List[Post] = session.query(Post).all()
    for post in post_objs:
        session.delete(post)
    session.commit()

    post_objs: List[Post] = session.query(Post).all()

    posts_serialized = PostSchema().dump(post_objs, many=True)

    session.close()

    return standard_response(data=posts_serialized, status_code=204)
