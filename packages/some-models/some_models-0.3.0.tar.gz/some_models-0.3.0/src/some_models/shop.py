from sqlalchemy import Column, String

from some_models.base import BaseModelOrm


class ShopOrm(BaseModelOrm):
    __tablename__ = "shop"

    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    # photo = Column(LargeBinary)
    # products = relationship("ProductOrm", back_populates="shop")
