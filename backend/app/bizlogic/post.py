import logging

import requests

from app.database.engine import DBsession
from app.database.models import Post, User

logger = logging.getLogger(__name__)


def fetch_and_save_posts():
    """
    Fetch Post data and user info using user_id from post and /users endpoint.

    endpoints used are
    https://jsonplaceholder.typicode.com/posts
    https://jsonplaceholder.typicode.com/users/<int:user_id>
    """

    logger.info("Start: fetch_and_save_posts")
    session = DBsession()

    try:
        # Fetch posts from API
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts", timeout=30
        )
        response.raise_for_status()
        posts_data = response.json()

        logger.info(f"Fetched {len(posts_data)} posts from API")

        for post_data in posts_data:
            print(f"Post: {post_data["id"]}")
            existing_post = session.query(Post).filter_by(id=post_data["id"]).first()

            if existing_post:
                logger.debug(f"Post {post_data['id']} exists")
                continue

            user = session.query(User).filter_by(id=post_data["userId"]).first()
            if user:
                new_post = Post(
                    id=post_data["id"],
                    user_id=user.id,
                    title=post_data["title"],
                    body=post_data["body"],
                    deleted=False,
                )
                session.add(new_post)
                session.commit()
            else:
                response = requests.get(
                    f"https://jsonplaceholder.typicode.com/users/{post_data['userId']}",
                    timeout=30,
                )
                response.raise_for_status()
                user_data = response.json()

                new_user = User(
                    id=user_data["id"],
                    name=user_data.get("name"),
                    email=user_data.get("email"),
                    phone_number=user_data.get("phone"),
                )
                session.add(new_user)
                
                session.flush()
                new_post = Post(
                    id=post_data["id"],
                    user_id=new_user.id,
                    title=post_data["title"],
                    body=post_data["body"],
                    deleted=False,
                )
                session.add(new_post)
                session.commit()
    

    except Exception as e:
        logger.error(f"Error processing posts data: {str(e)}")
        session.rollback()
    finally:
        session.close()
        logger.info("Complete: fetch_and_save_posts")
