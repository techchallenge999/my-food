from typing import List, Optional

from my_food.adapters.postgresql.models.order.order import OrderItemModel, OrderModel
from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
    OrderInterface,
)
from my_food.application.domain.aggregates.order.interfaces.order_repository import (
    OrderItemRepositoryDto,
    OrderRepositoryDto,
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):
    def create(self, entity: OrderInterface) -> None:
        new_order = OrderModel(
            status=OrderStatus.RECEIVED,
            total_amount=entity.total_amount,
            uuid=entity.uuid,
            user_uuid=entity.user_uuid,
        )
        new_order.create()
        for item in entity.items:
            new_order_item = OrderItemModel(
                comment=item.comment,
                order_uuid=entity.uuid,
                product_uuid=item.product_uuid,
                quantity=item.quantity,
            )
            new_order_item.create()

    def find(self, uuid: str) -> Optional[OrderRepositoryDto]:
        order = OrderModel.retrieve(uuid)
        if order is None:
            return None
        return OrderRepositoryDto(
            items=[
                OrderItemRepositoryDto(
                    comment=item.comment,
                    product_uuid=str(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            user_uuid=str(order.user_uuid),
            uuid=str(order.uuid),
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

    def list(self, filters={}) -> Optional[OrderRepositoryDto]:
        orders = OrderModel.list_filtering_by_column(filters, ["items"])
        if orders is None:
            return []

        return [
            OrderRepositoryDto(
                items=[
                    OrderItemRepositoryDto(
                        comment=item.comment,
                        product_uuid=str(item.product_uuid),
                        quantity=item.quantity,
                    )
                    for item in order[0].items
                ],
                status=order[0].status,
                total_amount=order[0].total_amount,
                uuid=str(order[0].uuid),
                user_uuid=str(order[0].user_uuid),
            )
            for order in orders
        ]

    def delete(self, uuid: str) -> Optional[OrderRepositoryDto]:
        order = OrderModel.retrieve(uuid)
        if order is None:
            return None
        OrderModel.destroy(order.uuid)
        return OrderRepositoryDto(
            items=[
                OrderItemRepositoryDto(
                    comment=item.comment,
                    product_uuid=str(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            uuid=str(order.uuid),
        )

    def filter_by_status(
        self, status: OrderStatus
    ) -> Optional[List[OrderRepositoryDto]]:
        orders = OrderModel.list_filtering_by_column({"status": status})
        if orders is None:
            return []

        return [
            OrderRepositoryDto(
                items=order.items,
                status=order.status,
                total_amount=order.total_amount,
                uuid=str(order.uuid),
            )
            for order in orders
        ]
