from dataclasses import dataclass
from my_food.application.domain.aggregates.payment.interfaces.payment_entity import (
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
