from typing import List, Optional

from my_food.application.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from my_food.application.domain.shared.errors.exceptions.payment import NoPaymentFoundException
from my_food.application.use_cases.payment.list.list_payment_dto import ListPaymentOutputDto


class ListPaymentUseCase:
    def __init__(self, repository: PaymentRepositoryInterface):
        self._repository = repository

    def execute(self) -> Optional[List[ListPaymentOutputDto]]:
        payments_list = self._repository.list()

        if payments_list is None:
            raise NoPaymentFoundException()

        return [
            ListPaymentOutputDto(
                order_uuid=payment.order_uuid,
                status=payment.status,
                uuid=payment.uuid,
            )
            for payment in payments_list
        ]
