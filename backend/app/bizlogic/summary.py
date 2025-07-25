import logging
from collections import Counter
from typing import Dict, List, Optional, Set

import nltk
from sqlalchemy.orm import Session

from app.api.schemas import UserSchema
from app.database.models import User

nltk.download("stopwords")
from nltk.corpus import stopwords

stop_words_nltk = set(stopwords.words("english"))

logger = logging.getLogger(__name__)


def get_words(text: str, use_nltk_stop_words=False) -> Set[str]:
    logger.info("running: get_words")
    """Extract unique words from text"""
    cleaned = text
    # Filter out short words and common stop words
    stop_words = {
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
    }
    if use_nltk_stop_words:
        stop_words = stop_words_nltk

    return set(
        word for word in cleaned.split() if len(word) > 2 and word not in stop_words
    )


def count_words(word_list: List[str], limit: Optional[int] = None):
    logger.info("running: count_words")

    word_counts = Counter(word_list)
    most_common = word_counts.most_common(limit) if limit else word_counts.most_common()

    return [{"name": word, "count": count} for word, count in most_common]


def count_all_users_words_from_titles(
    limit: Optional[int] = None, session: Optional[Session] = None
):
    logger.info("running:count_all_users_words_from_titles")
    if session is None:
        raise ValueError("Session cannot be None")

    users = session.query(User).all()
    word_list = []

    for user in users:
        posts = user.posts.all()
        for post in posts:
            if post.title:
                word_list.extend(list(get_words(post.title)))

    return count_words(word_list=word_list, limit=limit)


def identify_users_with_most_unique_titles_detailed(
    max_number_of_users: int = 3, session: Optional[Session] = None
) -> Dict:
    """
    Same as above but returns detailed information including the actual words.
    """
    if session is None:
        raise ValueError("Database session is required")

    users = session.query(User).all()
    user_data = []

    for user in users:
        user_words = set()
        posts = user.posts.all()

        for post in posts:
            if post.title:
                post_words = get_words(post.title)
                user_words = user_words.union(post_words)

        user_data.append(
            {
                "user_id": user.id,
                "unique_word_count": len(user_words),
                "unique_words": sorted(user_words),
                "post_count": len(posts),
                "user": UserSchema().dump(user),
            }
        )

    # Sort and return top users
    sorted_users = sorted(user_data, key=lambda x: x["unique_word_count"], reverse=True)

    output = {"top_users": sorted_users[:max_number_of_users]}
    return output
