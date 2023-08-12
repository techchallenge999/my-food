from src.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
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


class PaymentController:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    def pay_order(self, input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
        create_use_case = CreatePaymentUseCase(
            self.order_repository, self.product_repository, self.user_repository
        )
        payment = create_use_case.execute(input_data)
        return payment
