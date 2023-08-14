from uuid import UUID
from src.infrastructure.checkout.mock_checkout import MockCheckout
from src.domain.aggregates.order.entities.order import Order
from src.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
)

from src.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from src.domain.aggregates.order.value_objects.order_item import (
    OrderItem,
)
from src.domain.aggregates.payment.entities.payment import (
    PaymentStatus,
)
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)
from src.domain.shared.exceptions.order import (
    OrderNotFoundException,
)


class CreatePaymentUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository

    def execute(self, input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
        order = self._order_repository.find(input_data.order_uuid)
        if order is None:
            raise OrderNotFoundException()

        payment = MockCheckout.send_payment(input_data)
        if payment.status == PaymentStatus("pago"):
            updated_order = Order(
                items=[
                    OrderItem(
                        comment=item.comment,
                        product_uuid=UUID(item.product.uuid),
                        quantity=item.quantity,
                    )
                    for item in order.items
                ],
                order_repository=self._order_repository,
                product_repository=self._product_repository,
                user_repository=self._user_repository,
                status=OrderStatus("preparando"),
                user_uuid=UUID(order.user_uuid)
                if isinstance(order.user_uuid, str)
                else None,
                uuid=UUID(order.uuid),
            )
            self._order_repository.update(entity=updated_order)

        return CreatePaymentOutputDto(
            order_uuid=payment.order_uuid,
            status=payment.status,
            uuid=str(payment.uuid),
        )
