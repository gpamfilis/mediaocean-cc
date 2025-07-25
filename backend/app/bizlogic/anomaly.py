import logging

from fuzzywuzzy import fuzz

from app.api.schemas import PostSchema, UserSchema
from app.database.models import Post, User
from itertools import combinations

logger = logging.getLogger(__name__)


def anomaly_post_title_too_short(character_limit, session):
    anomalies = []
    # Get all posts for character limit check
    all_posts = session.query(Post).all()

    # Check for titles with less than character limit
    for post in all_posts:
        if len(post.title) < character_limit:
            anomalies.append(
                {
                    "user_id": post.user_id,
                    "flag_reason": "Title too short",
                    "post_title": post.title,
                    "post_id": post.id,
                    "user": UserSchema().dump(post.user),
                    "post": PostSchema(exclude=("user",)).dump(post),
                    "note": f"User post title {post.title} less than character limit: {character_limit}"
                }
            )
    return anomalies


def anomaly_duplicate_titles(session):
    anomalies = []
    for user in session.query(User).all():
        seen_titles = set()
        dup_titles = set()

        # First pass: find which titles occur more than once
        for post in user.posts.all():
            if post.title in seen_titles:
                dup_titles.add(post.title)
            else:
                seen_titles.add(post.title)
        for post in user.posts.all():
            if post.title in dup_titles:
                anomalies.append(
                    {
                        "user_id": user.id,
                        "flag_reason": "Duplicate Post",
                        "post_title": post.title,
                        "post_id": post.id,
                        "note": "User has duplicate title for their post."
                    }
                )
    return anomalies


def anomaly_similar_user_titles(similarity_threshold, min_posts, session):
    all_posts_info = [
        (post.id, post.title, post.user_id)
        for user in session.query(User).all()
        for post in user.posts
    ]

    flagged_posts = {}
    anomalies = []
    # TODO: use multiprocessing... this is not viable. Or move these to a worker to run.

    for (id1, title1, user1), (id2, title2, user2) in combinations(all_posts_info, 2):
        if user1 == user2:
            continue

        if fuzz.ratio(title1, title2) < similarity_threshold:
            continue

        post1 = (user1, id1, title1)
        post2 = (user2, id2, title2)

        for user_id, post_id, title in [post1, post2]:
            if user_id not in flagged_posts:
                flagged_posts[user_id] = set()

            if post_id not in flagged_posts[user_id]:
                flagged_posts[user_id].add(post_id)
                anomalies.append(
                    {
                        "user_id": user_id,
                        "flag_reason": "Similar Post",
                        "post_title": title,
                        "post_id": post_id,
                        "note": f"user {user_id} has {min_posts}+ posts with titles similar to other users (≥ {similarity_threshold}% match)",
                    }
                )

    return [
        a
        for a in anomalies
        if len(flagged_posts.get(a["user_id"])) >= min_posts
    ]


def get_anomaly_objects(
    session,
    similarity_threshold=50,
    min_posts=5,
    character_limit=15,
    sort_by="user_id",
    sort_order="asc",
):
    """
    Returns a list of anomaly objects with format:
    {"user_id", "flag_reason", "post_title", "post_id"}
    """
    logger.info("running:get_anomaly_objects")
    anomalies = []

    anomalies.extend(
        anomaly_post_title_too_short(character_limit=character_limit, session=session)
    )

    anomalies.extend(
        anomaly_similar_user_titles(similarity_threshold, min_posts, session)
    )

    anomalies.extend(anomaly_duplicate_titles(session))

    # unique = []
    # seen = set()

    # for entry in anomalies:
    #     key = (entry["user_id"], entry["post_id"], entry["flag_reason"])
    #     if key not in seen:
    #         seen.add(key)
    #         unique.append(entry)

    if sort_order == "asc":
        sort_order = False
    else:
        sort_order = True

    return sorted(anomalies, key=lambda x: x[sort_by], reverse=sort_order)
