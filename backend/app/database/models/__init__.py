import logging
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class DateMixin:
    created_at = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(Base, DateMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)
    posts = relationship("Post", back_populates="user", lazy="dynamic")


class Post(Base, DateMixin):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    deleted = Column(Boolean, default=False)
    user = relationship("User", back_populates="posts")
