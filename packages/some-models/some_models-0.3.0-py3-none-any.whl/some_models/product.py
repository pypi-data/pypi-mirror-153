from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from some_models.base import BaseModelOrm


class ProductOrm(BaseModelOrm):
    __tablename__ = "product"

    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"))
    shop = relationship("ShopOrm", back_populates="products")
