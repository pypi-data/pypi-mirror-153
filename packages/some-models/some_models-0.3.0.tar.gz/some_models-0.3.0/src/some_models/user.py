from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import Session

# from edulib.models import BaseModelOrm
# from auth.utils import get_password_hash

from some_models.base import BaseModelOrm


class UserOrm(BaseModelOrm):
    __tablename__ = "user"

    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return (
            f"UserOrm(id={self.id!r}, username={self.username!r}, "
            f"hashed_password={self.hashed_password!r}, email={self.email!r})"
        )

    @classmethod
    def get_user_by_username(
        cls, db: Session, username: str
    ) -> Optional["UserOrm"]:
        return db.query(cls).filter(cls.username == username).first()
