from typing import Optional
from src.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from src.domain.aggregates.payment.interfaces.payment_repository import (
    PaymentRepositoryInterface,
)
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
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
    def checkout(
        self,
        input_data: CreatePaymentInputDto,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> CreatePaymentOutputDto:
        create_use_case = CreatePaymentUseCase(
            order_repository, product_repository, user_repository
        )
        payment = create_use_case.execute(input_data)
        return payment

    def get_payment_status(
        self, order_uuid: str, payment_repository: PaymentRepositoryInterface
    ) -> Optional[FindPaymentOutputDto]:
        find_use_case = FindPaymentByOrderUseCase(payment_repository)
        payment = find_use_case.execute(FindPaymentByOrderInputDto(order_uuid))
        return payment

    def webhook(
        self,
        input_data: UpdatePaymentInputDto,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
    ) -> Optional[UpdatePaymentOutputDto]:
        update_use_case = UpdatePaymentUseCase(payment_repository, order_repository)
        payment = update_use_case.execute(input_data)
        return payment
