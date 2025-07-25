import logging
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine

from sqlalchemy.orm import sessionmaker

from app.database.models import Base

logger = logging.getLogger(__name__)


engine: Engine = None  # type: ignore
DBsession = sessionmaker(expire_on_commit=False)

SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"


def init_db(url: str):
    engine = create_engine(
        url,
        # poolclass=NullPool,
        pool_pre_ping=True,  # Enable pre-ping to avoid stale connections
        pool_recycle=1800,  # Recycle connections after 1800 seconds
        echo=SQLALCHEMY_ECHO,
    )  # max_overflow=-1,
    Base.metadata.bind = engine  # type: ignore
    DBsession.bind = engine  # type: ignore
