from uuid import UUID

from src.domain.aggregates.payment.interfaces.payment import PaymentStatus
from src.domain.aggregates.payment.entities.payment import Payment
from src.domain.shared.exceptions.payment import (
    InvalidPaymentStatusException,
    PaymentNotFoundException,
)
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.use_cases.order.update.update_order import UpdateOrderUseCase
from src.use_cases.payment.update.update_payment_dto import (
    UpdatePaymentInputDto,
    UpdatePaymentOutputDto,
)


class UpdatePaymentUseCase:
    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
        update_order_status_use_case: UpdateOrderUseCase,
    ):
        self._payment_repository = payment_repository
        self._order_repository = order_repository
        self._update_order_status_use_case = update_order_status_use_case

    def execute(
        self, payment_uuid: str, input_data: UpdatePaymentInputDto
    ) -> UpdatePaymentOutputDto:
        payment = self._payment_repository.find(payment_uuid)

        if payment is None:
            raise PaymentNotFoundException()

        updated_payment = Payment(
            order_uuid=UUID(payment.order_uuid),
            order_repository=self._order_repository,
            status=input_data.status,
            uuid=UUID(payment.uuid),
        )

        updated_payment_dto = UpdatePaymentOutputDto(
            order_uuid=updated_payment.order_uuid,
            status=updated_payment.status,
            uuid=updated_payment.uuid,
        )

        self._payment_repository.update(updated_payment_dto)
        self.update_order_status(
            updated_payment_dto.order_uuid, updated_payment_dto.status
        )

        return updated_payment_dto

    def update_order_status(
        self, order_uuid: str, new_payment_status: PaymentStatus
    ) -> None:
        match new_payment_status:
            case PaymentStatus.PAID:
                self._update_order_status_use_case.progress_status(order_uuid)
            case PaymentStatus.REFUSED:
                self._update_order_status_use_case.cancel(order_uuid)
            case _:
                raise InvalidPaymentStatusException()
