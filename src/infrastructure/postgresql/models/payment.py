import uuid

from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.domain.aggregates.payment.interfaces.payment import PaymentStatus
from src.infrastructure.postgresql.database import Base
from src.infrastructure.postgresql.models.order import OrderModel
from src.infrastructure.postgresql.repositories.mixins import CRUDMixin


class PaymentModel(Base, CRUDMixin):
    __tablename__ = "payment"

    order_uuid = Column(UUID(as_uuid=True), ForeignKey(OrderModel.__table__.c.uuid))
    status = Column(Enum(PaymentStatus), index=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)
