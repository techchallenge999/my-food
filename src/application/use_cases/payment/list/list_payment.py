from typing import List, Optional

from src.application.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from src.application.domain.shared.errors.exceptions.payment import NoPaymentFoundException
from src.application.use_cases.payment.list.list_payment_dto import ListPaymentOutputDto


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
