import logging

from fuzzywuzzy import fuzz

from app.api.schemas import PostSchema, UserSchema
from app.database.models import Post, User

logger = logging.getLogger(__name__)


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
                }
            )

    # Check for similar posts by user
    for user in session.query(User).all():
        user_posts = user.posts.all()

        if len(user_posts) < min_posts:
            continue

        # Check for similar titles within user's posts
        for i, post1 in enumerate(user_posts):
            for post2 in user_posts[i + 1 :]:
                similarity_score = fuzz.ratio(post1.title.lower(), post2.title.lower())

                if similarity_score >= similarity_threshold:
                    # Add both posts as anomalies
                    anomalies.append(
                        {
                            "user_id": user.id,
                            "flag_reason": "Similar Post",
                            "post_title": post1.title,
                            "post_id": post1.id,
                        }
                    )

    # Duplicate Titles.
    for user in session.query(User).all():
        seen_titles = set()
        dup_titles = set()

        # First pass: find which titles occur more than once
        for post in user.posts.all():
            if post.title in seen_titles:
                dup_titles.add(post.title)
            else:
                seen_titles.add(post.title)

        # Second pass: record each post whose title was duplicated
        for post in user.posts.all():
            if post.title in dup_titles:
                anomalies.append(
                    {
                        "user_id": user.id,
                        "flag_reason": "Duplicate Post",
                        "post_title": post.title,
                        "post_id": post.id,
                    }
                )

    unique = []
    seen = set()

    for entry in anomalies:
        # define what makes an entry “duplicate”
        key = (entry["user_id"], entry["post_id"], entry["flag_reason"])
        if key not in seen:
            seen.add(key)
            unique.append(entry)

    if sort_order == "asc":
        sort_order = False
    else:
        sort_order = True

    return sorted(unique, key=lambda x: x[sort_by], reverse=sort_order)
