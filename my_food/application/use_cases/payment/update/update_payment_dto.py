from dataclasses import dataclass
from my_food.application.domain.aggregates.payment.entities.payment import PaymentStatus


@dataclass
class UpdatePaymentInputDto:
    status: PaymentStatus
    uuid: str


@dataclass
class UpdatePaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
