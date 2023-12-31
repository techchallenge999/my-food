from src.domain.shared.exceptions.payment import PaymentNotFoundException
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.use_cases.payment.find.find_payment_dto import (
    FindPaymentByOrderInputDto,
    FindPaymentInputDto,
    FindPaymentOutputDto,
)


class FindPaymentUseCase:
    def __init__(self, repository: PaymentRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindPaymentInputDto) -> FindPaymentOutputDto:
        payment = self._repository.find(uuid=input_data.uuid)

        if payment is None:
            raise PaymentNotFoundException()

        return FindPaymentOutputDto(
            order_uuid=payment.order_uuid,
            status=payment.status,
            uuid=payment.uuid,
        )


class FindPaymentByOrderUseCase:
    def __init__(self, repository: PaymentRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindPaymentByOrderInputDto) -> FindPaymentOutputDto:
        payment = self._repository.find_by_order(order_uuid=input_data.order_uuid)

        if payment is None:
            raise PaymentNotFoundException()

        return FindPaymentOutputDto(
            order_uuid=payment.order_uuid,
            status=payment.status,
            uuid=payment.uuid,
        )
