from dataclasses import dataclass

from src.domain.aggregates.payment.interfaces.payment import (
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


@dataclass
class FindPaymentByOrderInputDto:
    order_uuid: str
