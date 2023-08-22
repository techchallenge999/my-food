from dataclasses import dataclass
from src.domain.aggregates.payment.interfaces.payment_entity import PaymentStatus


@dataclass
class UpdatePaymentInputDto:
    status: PaymentStatus


@dataclass
class UpdatePaymentOutputDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str
