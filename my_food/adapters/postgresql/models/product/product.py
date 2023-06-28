import uuid
from sqlalchemy import Column, Integer, String, Enum, Float, BLOB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from my_food.adapters.postgresql.database import Base, engine
from my_food.adapters.postgresql.repositories.mixins.crud import CRUDMixin
from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


class ProductModel(Base, CRUDMixin):
    __tablename__ = "product"

    name = Column(String, nullable=False)
    category = Column(Enum(ProductCategory), index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    image = Column(BLOB)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)
    order_items = relationship('OrderItemModel')


ProductModel.metadata.bind = engine
ProductModel.metadata.create_all(engine)
