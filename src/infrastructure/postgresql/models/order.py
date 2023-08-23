import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.domain.aggregates.order.interfaces.value_objects import OrderStatus
from src.infrastructure.postgresql.database import Base
from src.infrastructure.postgresql.models.timestamp import BaseTimestamp
from src.infrastructure.postgresql.repositories.mixins import CRUDMixin
from src.infrastructure.postgresql.repositories.product import ProductModel


class OrderModel(Base, CRUDMixin, BaseTimestamp):
    __tablename__ = "order"

    items = relationship(
        "OrderItemModel", lazy="subquery", cascade="all, delete-orphan"
    )
    status = Column(
        Enum(OrderStatus), default=OrderStatus.PENDING_PAYMENT, nullable=False
    )
    total_amount = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), nullable=True)
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class OrderItemModel(Base, CRUDMixin):
    __tablename__ = "orderitem"

    comment = Column(String)
    order_uuid = Column(UUID(as_uuid=True), ForeignKey("order.uuid"))
    product_uuid = Column(UUID(as_uuid=True), ForeignKey(ProductModel.__table__.c.uuid))
    quantity = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    product = relationship(ProductModel, back_populates="order_items")
