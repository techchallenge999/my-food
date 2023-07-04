import uuid
from sqlalchemy import Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from my_food.adapters.postgresql.database import Base
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
    image = Column(BYTEA)
    is_active = Column(Boolean)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)
    order_items = relationship("OrderItemModel")
