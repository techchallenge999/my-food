from dataclasses import dataclass
from src.application.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentStatus,
)


@dataclass
class CreatePaymentInputDto:
    order_uuid: str


@dataclass
class CreatePaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
