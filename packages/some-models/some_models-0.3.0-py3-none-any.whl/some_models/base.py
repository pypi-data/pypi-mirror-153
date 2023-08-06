from dataclasses import dataclass
from typing import Any

from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, Session, DeclarativeMeta, Query
from sqlalchemy.sql import func

Base: DeclarativeMeta = declarative_base()


@dataclass(frozen=True, slots=True)
class Page:
    total: int
    offset: int
    limit: int | None
    items: list[Base]


class BaseModelOrm(Base):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.current_timestamp(),
    )
    is_active = Column(Boolean, nullable=False, default=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    @classmethod
    def _get_filtered_query(cls, db: Session, **kwargs: Any) -> Query:
        """Добавляет все фильтры к запросу в базу данных"""
        query = db.query(cls)
        for key, value in kwargs.items():
            obj_attr = getattr(cls, key, None)
            if obj_attr and value:
                query = query.filter(obj_attr == value)
        return query

    @classmethod
    def _get_objects_with_offset_limit(
        cls, query: Query, offset: int = 0, limit: int | None = 50
    ) -> list["BaseModelOrm"]:
        """Для получения объектов с пагинацией"""
        return query.offset(offset).limit(limit).all()

    @classmethod
    def get_list(cls, db: Session, **kwargs: Any) -> list["BaseModelOrm"]:
        """Для фильтрации без пагинации"""
        query = cls._get_filtered_query(db, **kwargs)
        return cls._get_objects_with_offset_limit(query, 0, None)

    @classmethod
    def get_page(
        cls,
        db: Session,
        offset: int = 0,
        limit: int | None = 50,
        **kwargs: Any,
    ) -> Page:
        """Для фильтрации с пагинацией"""

        query = cls._get_filtered_query(db, **kwargs)
        total = query.count()
        items = cls._get_objects_with_offset_limit(query, offset, limit)
        return Page(total, offset, limit, items)

    @classmethod
    def create(cls, db: Session, kwargs: dict) -> "BaseModelOrm":
        item = cls(**kwargs)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @classmethod
    def get_by_id(cls, db: Session, id_: int) -> "BaseModelOrm":
        return cls.get_list(db, id=id_)[0]

    @classmethod
    def update(cls, db: Session, id_: int, kwargs: dict) -> "BaseModelOrm":
        item = db.query(cls).filter(cls.id == id_).one()

        for k, v in kwargs.items():
            if hasattr(item, k):
                setattr(item, k, v)

        db.commit()
        db.refresh(item)

        return item

    @classmethod
    def delete(cls, db: Session, id_: int) -> int:
        count = db.query(cls).filter(cls.id == id_).delete()
        db.commit()
        return count
