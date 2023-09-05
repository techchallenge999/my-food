from dataclasses import dataclass

from src.domain.aggregates.payment.interfaces.payment import (
    PaymentStatus,
)


@dataclass
class ListPaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
