from typing import List, Optional

from my_food.adapters.postgresql.models.order.order import OrderModel
from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
    OrderInterface,
)
from my_food.application.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryDto,
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):
    def create(self, entity: OrderInterface) -> None:
        new_order = OrderModel(
            status=OrderStatus.RECEIVED,
            total_amount=entity.total_amount,
            uuid=entity.uuid,
        )
        new_order.create()

    def find(self, uuid: str) -> Optional[OrderRepositoryDto]:
        order = OrderModel.retrieve(uuid)
        if order is None:
            return None
        return OrderRepositoryDto(
            items=order.items,
            status=order.status,
            total_amount=order.total_amount,
            uuid=order.uuid,
        )

    def update(self, entity: OrderInterface) -> None:
        order = OrderModel.retrieve(entity.uuid)
        if order:
            OrderModel.update(
                {
                    "items": entity.items,
                    "status": entity.status,
                    "total_amount": entity.total_amount,
                    "uuid": entity.uuid,
                    "id": order.id,
                }
            )

    def list(self) -> Optional[OrderRepositoryDto]:
        orders = OrderModel.list()

        return [
            OrderRepositoryDto(
                items=order.items,
                status=order.status,
                total_amount=order.total_amount,
                uuid=order.uuid,
            )
            for order in orders
        ]

    def delete(self, uuid: str) -> Optional[OrderRepositoryDto]:
        order = OrderModel.retrieve(uuid)
        if order is None:
            return None
        OrderModel.destroy(order.uuid)
        return OrderRepositoryDto(
            items=order.items,
            status=order.status,
            total_amount=order.total_amount,
            uuid=order.uuid,
        )

    def filter_by_status(
        self, status: OrderStatus
    ) -> Optional[List[OrderRepositoryDto]]:
        orders = OrderModel.list_filtering_by_column({"status": status})

        return [
            OrderRepositoryDto(
                items=order.items,
                status=order.status,
                total_amount=order.total_amount,
                uuid=order.uuid,
            )
            for order in orders
        ]
