import uuid

from sqlalchemy import Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship

from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.infrastructure.postgresql.database import Base
from src.infrastructure.postgresql.repositories.mixins import CRUDMixin


class ProductModel(Base, CRUDMixin):
    __tablename__ = "product"

    name = Column(String, nullable=False)
    category = Column(Enum(ProductCategory), index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    image = Column(BYTEA)
    is_active = Column(Boolean, default=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)
    order_items = relationship("OrderItemModel", back_populates="product")
