from typing import Optional
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus
from src.domain.aggregates.payment.interfaces.payment_entity import PaymentStatus
from src.domain.shared.exceptions.payment import InvalidPaymentStatusException

from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.order.update.update_order import UpdateOrderStatusUseCase
from src.use_cases.order.update.update_order_dto import UpdateOrderStatusInputDto
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
        payment_uuid: str,
        input_data: UpdatePaymentInputDto,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> Optional[UpdatePaymentOutputDto]:
        update_payment_use_case = UpdatePaymentUseCase(
            self.repository, order_repository
        )
        payment = update_payment_use_case.execute(payment_uuid, input_data)

        if payment.status == PaymentStatus.PAID:
            new_order_status = OrderStatus.RECEIVED
        elif payment.status == PaymentStatus.REFUSED:
            new_order_status = OrderStatus.CANCELED
        else:
            raise InvalidPaymentStatusException()

        update_order_use_case = UpdateOrderStatusUseCase(
            order_repository, product_repository, user_repository
        )
        update_order_use_case.execute(
            payment.order_uuid, UpdateOrderStatusInputDto(status=new_order_status)
        )

        return payment
