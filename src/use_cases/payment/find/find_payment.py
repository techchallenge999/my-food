from typing import Optional

from src.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from src.domain.shared.exceptions.payment import PaymentNotFoundException
from src.use_cases.payment.find.find_payment_dto import FindPaymentInputDto, FindPaymentOutputDto


class FindPaymentUseCase:
    def __init__(self, repository: PaymentRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindPaymentInputDto) -> Optional[FindPaymentOutputDto]:
        payment = self._repository.find(uuid=input_data.uuid)

        if payment is None:
            raise PaymentNotFoundException()

        return FindPaymentOutputDto(
            order_uuid=payment.order_uuid,
            status=payment.status,
            uuid=payment.uuid,
        )
