from dataclasses import dataclass
from my_food.application.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentStatus,
)


@dataclass
class FindPaymentInputDto:
    uuid: str


@dataclass
class FindPaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
