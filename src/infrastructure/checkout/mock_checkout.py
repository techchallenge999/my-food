from uuid import uuid4

from src.domain.aggregates.payment.interfaces.payment_entity import PaymentStatus
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)


class MockCheckout:
    @staticmethod
    def send_payment(pagamento: CreatePaymentInputDto) -> CreatePaymentOutputDto:
        return CreatePaymentOutputDto(
            order_uuid=pagamento.order_uuid, status=PaymentStatus("pago"), uuid=uuid4()
        )
