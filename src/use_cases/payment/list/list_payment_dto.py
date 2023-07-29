from dataclasses import dataclass
from src.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentStatus,
)


@dataclass
class ListPaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
