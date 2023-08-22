from uuid import UUID
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus
from src.domain.aggregates.payment.interfaces.payment_entity import PaymentStatus

from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.domain.aggregates.payment.entities.payment import Payment
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.domain.shared.exceptions.payment import (
    InvalidPaymentStatusException,
    PaymentNotFoundException,
)
from src.use_cases.order.update.update_order import UpdateOrderStatusUseCase
from src.use_cases.order.update.update_order_dto import UpdateOrderStatusInputDto
from src.use_cases.payment.update.update_payment_dto import (
    UpdatePaymentInputDto,
    UpdatePaymentOutputDto,
)


class UpdatePaymentUseCase:
    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
        update_order_status_use_case: UpdateOrderStatusUseCase,
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

        self._payment_repository.update(entity=updated_payment)

        self.update_order_status(updated_payment.order_uuid, updated_payment.status)

        return UpdatePaymentOutputDto(
            order_uuid=updated_payment.order_uuid,
            status=updated_payment.status,
            uuid=updated_payment.uuid,
        )

    def update_order_status(
        self, order_uuid: str, new_payment_status: PaymentStatus
    ) -> None:
        match new_payment_status:
            case PaymentStatus.PAID:
                new_order_status = OrderStatus.RECEIVED
            case PaymentStatus.REFUSED:
                new_order_status = OrderStatus.CANCELED
            case _:
                raise InvalidPaymentStatusException()
        self._update_order_status_use_case.execute(
            order_uuid, UpdateOrderStatusInputDto(status=new_order_status)
        )
