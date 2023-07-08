import uuid
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from my_food.adapters.postgresql.database import Base
from my_food.adapters.postgresql.repositories.mixins.crud import CRUDMixin
from my_food.adapters.postgresql.repositories.product.product import ProductModel
from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
)


class OrderModel(Base, CRUDMixin):
    __tablename__ = "order"

    items = relationship(
        "OrderItemModel", lazy="subquery", cascade="all, delete-orphan"
    )
    status = Column(Enum(OrderStatus), default=OrderStatus.RECEIVED, nullable=False)
    total_amount = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), nullable=True)
    id = Column(Integer, primary_key=True)


class OrderItemModel(Base, CRUDMixin):
    __tablename__ = "orderitem"

    comment = Column(String)
    order_uuid = Column(UUID(as_uuid=True), ForeignKey("order.uuid"))
    product_uuid = Column(UUID(as_uuid=True), ForeignKey(ProductModel.__table__.c.uuid))
    quantity = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    product = relationship(ProductModel, back_populates="order_items")
