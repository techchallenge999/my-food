from typing import Optional
from uuid import UUID

from src.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from src.domain.aggregates.payment.entities.payment import Payment
from src.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from src.domain.shared.errors.exceptions.payment import PaymentNotFoundException
from src.use_cases.payment.update.update_payment_dto import UpdatePaymentInputDto, UpdatePaymentOutputDto


class UpdatePaymentUseCase:
    def __init__(
            self,
            payment_repository: PaymentRepositoryInterface,
            order_repository: OrderRepositoryInterface,
        ):
        self._payment_repository = payment_repository
        self._order_repository = order_repository

    def execute(self, input_data: UpdatePaymentInputDto) -> Optional[UpdatePaymentOutputDto]:
        payment = self._payment_repository.find(input_data.uuid)

        if payment is None:
            raise PaymentNotFoundException()

        updated_payment = Payment(
            order_uuid=UUID(payment.order_uuid),
            payment_repository=self._payment_repository,
            order_repository=self._order_repository,
            status=input_data.status,
            uuid=UUID(payment.uuid),
        )

        self._payment_repository.update(entity=updated_payment)

        return UpdatePaymentOutputDto(
            order_uuid=updated_payment.order_uuid,
            status=updated_payment.status,
            uuid=updated_payment.uuid,
        )
