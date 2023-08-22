import os
from uuid import UUID

from src.domain.aggregates.payment.entities.payment import Payment
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.interface_adapters.gateways.payment_gateways import PaymentGatewayInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)


class CreatePaymentUseCase:
    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
        payment_gateway: PaymentGatewayInterface,
    ):
        self._payment_repository = payment_repository
        self._order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
        order = self._order_repository.find(input_data.order_uuid)

        if order is None:
            raise OrderNotFoundException()

        new_payment = Payment(
            UUID(order.uuid),
            self._order_repository,
        )

        self._payment_repository.create(entity=new_payment)
        payment_gateway_data = self.payment_gateway.create(
            f"{os.getenv('API_URL', 'http://localhost:8000')}/webhook/{new_payment.uuid}"
        )

        return CreatePaymentOutputDto(
            order_uuid=new_payment.order_uuid,
            status=new_payment.status,
            uuid=new_payment.uuid,
            qr_data=payment_gateway_data.qr_data,
        )
