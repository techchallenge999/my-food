from src.interface_adapters.gateways.payment_gateway import PaymentGatewayInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.order.find.find_order import FindOrderUseCase
from src.use_cases.order.update.update_order import UpdateOrderUseCase
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
    def __init__(
        self,
        repository: PaymentRepositoryInterface,
        payment_gateway: PaymentGatewayInterface,
    ):
        self.repository = repository
        self.payment_gateway = payment_gateway

    def checkout(
        self,
        input_data: CreatePaymentInputDto,
        order_repository: OrderRepositoryInterface,
    ) -> CreatePaymentOutputDto:
        create_use_case = CreatePaymentUseCase(
            self.repository, order_repository, self.payment_gateway
        )
        payment = create_use_case.execute(input_data)
        return payment

    def get_payment_status(self, order_uuid: str) -> FindPaymentOutputDto | None:
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
    ) -> UpdatePaymentOutputDto:
        update_use_case = UpdatePaymentUseCase(
            self.repository,
            order_repository,
            UpdateOrderUseCase(
                order_repository,
                product_repository,
                user_repository,
                FindOrderUseCase(order_repository),
            ),
        )
        payment = update_use_case.execute(payment_uuid, input_data)
        return payment
