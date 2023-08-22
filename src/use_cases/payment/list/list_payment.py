from typing import List, Optional

from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.domain.shared.exceptions.payment import NoPaymentFoundException
from src.use_cases.payment.list.list_payment_dto import ListPaymentOutputDto


class ListPaymentUseCase:
    def __init__(self, repository: PaymentRepositoryInterface):
        self._repository = repository

    def execute(self) -> Optional[List[ListPaymentOutputDto]]:
        payment_list = self._repository.list()

        if payment_list is None:
            raise NoPaymentFoundException()

        return [
            ListPaymentOutputDto(
                order_uuid=payment.order_uuid,
                status=payment.status,
                uuid=payment.uuid,
            )
            for payment in payment_list
        ]
