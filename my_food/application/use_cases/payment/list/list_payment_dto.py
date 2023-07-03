from dataclasses import dataclass
from my_food.application.domain.aggregates.payment.entities.payment import PaymentStatus


@dataclass
class ListPaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
