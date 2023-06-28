import uuid
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from my_food.adapters.postgresql.database import Base, engine
from my_food.adapters.postgresql.repositories.mixins.crud import CRUDMixin
from my_food.application.domain.aggregates.order.interfaces.order_entity import OrderStatusCategory


class OrderModel(Base, CRUDMixin):
    __tablename__ = "order"

    items = relationship('OrderItemModel')
    status = Column(Enum(OrderStatusCategory), default=OrderStatusCategory.PREPARING, nullable=False)
    total_amount = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)


OrderModel.metadata.bind = engine
OrderModel.metadata.create_all(engine)


class OrderItemModel(Base, CRUDMixin):
    __tablename__ = "order"

    comment = Column(String)
    order_uuid = Column(UUID(as_uuid=True), ForeignKey('order.uuid'))
    product_uuid = Column(UUID(as_uuid=True), ForeignKey('product.uuid'))
    quantity = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)


OrderItemModel.metadata.bind = engine
OrderItemModel.metadata.create_all(engine)
