from dataclasses import asdict
from uuid import UUID

from src.domain.aggregates.order.entities.order import Order
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.aggregates.order.value_objects.order_item import OrderItem
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.domain.shared.exceptions.order import (
    OrderNotFoundException,
)
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderItemOutputDto,
    UpdateOrderOutputDto,
)
from src.use_cases.product.find.find_product_dto import (
    FindProductOutputDto,
)


class UpdateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository

    def execute(self, input_data: UpdateOrderInputDto) -> UpdateOrderOutputDto:
        order = self._order_repository.find(input_data.uuid)

        if order is None:
            raise OrderNotFoundException()

        updated_order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in input_data.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            status=input_data.status,
            user_uuid=UUID(order.user_uuid)
            if isinstance(order.user_uuid, str)
            else None,
            uuid=UUID(order.uuid),
        )

        self._order_repository.update(entity=updated_order)

        return UpdateOrderOutputDto(
            items=[
                UpdateOrderItemOutputDto(
                    comment=item.comment,
                    product=FindProductOutputDto(
                        **asdict(self._product_repository.find(item.product_uuid))
                    ),
                    quantity=item.quantity,
                )
                for item in updated_order.items
            ],
            status=updated_order.status,
            total_amount=updated_order.total_amount,
            user_uuid=updated_order.user_uuid,
            uuid=updated_order.uuid,
        )
