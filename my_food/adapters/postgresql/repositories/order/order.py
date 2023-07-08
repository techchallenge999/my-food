from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from my_food.adapters.postgresql.database import get_session
from my_food.adapters.postgresql.models.order.order import OrderItemModel, OrderModel
from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
    OrderInterface,
)
from my_food.application.domain.aggregates.order.interfaces.order_repository import (
    DeleteOrderItemRepositoryDto,
    OrderItemRepositoryDto,
    OrderRepositoryDto,
    OrderRepositoryInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
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
        with get_session() as session:
            stmt = select(OrderModel)
            stmt = stmt.options(
                subqueryload(OrderModel.items).options(
                    subqueryload(OrderItemModel.product)
                )
            )
            instance = session.execute(stmt.filter_by(uuid=UUID(uuid))).first()
            order = instance[0] if instance is not None else None
        if order is None:
            return None
        return OrderRepositoryDto(
            items=[
                OrderItemRepositoryDto(
                    comment=item.comment,
                    product=ProductRepositoryDto(
                        name=item.product.name,
                        category=item.product.category,
                        price=item.product.price,
                        description=item.product.description,
                        image=item.product.image,
                        is_active=item.product.is_active,
                        uuid=str(item.product.uuid),
                    ),
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            uuid=str(order.uuid),
            user_uuid=str(order.user_uuid),
        )

    def update(self, entity: OrderInterface) -> None:
        order = OrderModel.retrieve(entity.uuid)
        if order:
            for item in order.items:
                item.self_destroy()
            for item in entity.items:
                OrderItemModel(
                    comment=item.comment,
                    order_uuid=order.uuid,
                    product_uuid=item.product_uuid,
                    quantity=item.quantity,
                ).create()

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
        with get_session() as session:
            stmt = select(OrderModel)
            stmt = stmt.options(
                subqueryload(OrderModel.items).options(
                    subqueryload(OrderItemModel.product)
                )
            )

            for column in filters.keys():
                if not hasattr(OrderModel, column):
                    return None
                stmt = stmt.filter((getattr(OrderModel, column) == filters.get(column)))

            orders = session.execute(stmt).all()
        if orders is None:
            return []

        return [
            OrderRepositoryDto(
                items=[
                    OrderItemRepositoryDto(
                        comment=item.comment,
                        product=ProductRepositoryDto(
                            name=item.product.name,
                            category=item.product.category,
                            price=item.product.price,
                            description=item.product.description,
                            image=item.product.image,
                            is_active=item.product.is_active,
                            uuid=str(item.product.uuid),
                        ),
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
        OrderModel.destroy(str(order.uuid))
        return OrderRepositoryDto(
            items=[
                DeleteOrderItemRepositoryDto(
                    comment=item.comment,
                    product_uuid=str(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            uuid=str(order.uuid),
            user_uuid=str(order.user_uuid),
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
