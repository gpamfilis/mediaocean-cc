import logging
from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar, Union

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
IdType = Union[UUID, String, Integer]


T = TypeVar("T")
A = TypeVar("A")
U = TypeVar("U")


class Repository[T, A, U](ABC):
    """
    Abstract class for model operations.
    """

    @abstractmethod
    def __init__(self, user_id: IdType, session: Session) -> None:
        self.session = session
        self.user_id = user_id

    @abstractmethod
    def get(self, item_id: IdType) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, data: A) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, item_id: IdType, data: U) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: IdType) -> T:
        raise NotImplementedError
