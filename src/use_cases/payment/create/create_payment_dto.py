from dataclasses import dataclass

from src.domain.aggregates.payment.interfaces.payment import (
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
    qr_data: str
