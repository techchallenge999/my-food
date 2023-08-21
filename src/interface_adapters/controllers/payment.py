from typing import Optional

from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.use_cases.payment.create.create_payment import CreatePaymentUseCase
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)
from src.use_cases.payment.find.find_payment import FindPaymentByOrderUseCase
from src.use_cases.payment.find.find_payment_dto import (
    FindPaymentByOrderInputDto,
    FindPaymentOutputDto,
)
from src.use_cases.payment.update.update_payment import UpdatePaymentUseCase
from src.use_cases.payment.update.update_payment_dto import (
    UpdatePaymentInputDto,
    UpdatePaymentOutputDto,
)


class PaymentController:
    def __init__(self, repository: PaymentRepositoryInterface):
        self.repository = repository

    def checkout(
        self,
        input_data: CreatePaymentInputDto,
        order_repository: OrderRepositoryInterface,
    ) -> CreatePaymentOutputDto:
        create_use_case = CreatePaymentUseCase(self.repository, order_repository)
        payment = create_use_case.execute(input_data)
        return payment

    def get_payment_status(self, order_uuid: str) -> Optional[FindPaymentOutputDto]:
        find_use_case = FindPaymentByOrderUseCase(self.repository)
        payment = find_use_case.execute(FindPaymentByOrderInputDto(order_uuid))
        return payment

    def webhook(
        self,
        input_data: UpdatePaymentInputDto,
        order_repository: OrderRepositoryInterface,
    ) -> Optional[UpdatePaymentOutputDto]:
        update_use_case = UpdatePaymentUseCase(self.repository, order_repository)
        payment = update_use_case.execute(input_data)
        return payment
