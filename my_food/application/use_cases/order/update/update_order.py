from dataclasses import asdict
from typing import Optional
from uuid import UUID

from my_food.application.domain.aggregates.order.entities.order import Order, OrderItem
from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.product.interfaces.product_repository import ProductRepositoryInterface
from my_food.application.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderItemOutputDto,
    UpdateOrderOutputDto,
)
from my_food.application.use_cases.product.find.find_product_dto import FindProductOutputDto


class UpdateOrderUseCase:
    def __init__(
            self,
            order_repository: OrderRepositoryInterface,
            product_repository: ProductRepositoryInterface,
        ):
        self._order_repository = order_repository
        self._product_repository = product_repository

    def execute(self, input_data: UpdateOrderInputDto) -> Optional[UpdateOrderOutputDto]:
        order = self._order_repository.find(input_data.uuid)

        if order is None:
            return None

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
            status=input_data.status,
            uuid=UUID(order.uuid),
        )

        self._order_repository.update(entity=updated_order)

        return UpdateOrderOutputDto(
            items=[
                UpdateOrderItemOutputDto(
                    comment=item.comment,
                    product=FindProductOutputDto(**asdict(self._product_repository.find(item.product_uuid))),
                    quantity=item.quantity,
                )
                for item in updated_order.items
            ],
            status=updated_order.status,
            total_amount=updated_order.total_amount,
            uuid=updated_order.uuid,
        )
