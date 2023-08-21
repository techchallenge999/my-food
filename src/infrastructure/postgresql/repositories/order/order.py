from typing import List, Optional
from uuid import UUID

from sqlalchemy import case, select
from sqlalchemy.orm import subqueryload

from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.models.order.order import OrderItemModel, OrderModel
from src.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
    OrderInterface,
)
from src.interface_adapters.gateways.repositories.order import (
    OrderItemRepositoryDto,
    OrderRepositoryDto,
    OrderRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryDto,
)
from src.domain.shared.exceptions.order import (
    OrderNotFoundException,
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
            raise OrderNotFoundException()
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
            created_at=order.created_at,
            updated_at=order.updated_at,
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

    def list(
        self,
        filters: dict = {},
        exclusive_filters: dict = {},
    ) -> List[Optional[OrderRepositoryDto]]:
        with get_session() as session:
            stmt = select(OrderModel)
            stmt = stmt.options(
                subqueryload(OrderModel.items).options(
                    subqueryload(OrderItemModel.product)
                )
            )

            for column in filters.keys():
                if not hasattr(OrderModel, column):
                    return []
                stmt = stmt.filter(getattr(OrderModel, column) == filters.get(column))
            for column, values in exclusive_filters.items():
                if not hasattr(OrderModel, column):
                    return []
                for value in values:
                    stmt = stmt.filter(getattr(OrderModel, column) != value)

            stmt = stmt.order_by(OrderModel.created_at)
            stmt = stmt.order_by(
                case(
                    {
                        OrderModel.status == OrderStatus.READY: 0,
                        OrderModel.status == OrderStatus.PREPARING: 1,
                        OrderModel.status == OrderStatus.RECEIVED: 2,
                    },
                    else_=3,
                )
            )

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
                created_at=order[0].created_at,
                updated_at=order[0].updated_at,
            )
            for order in orders
        ]

    def delete(self, uuid: str) -> Optional[OrderRepositoryDto]:
        order = OrderModel.retrieve(uuid)
        if order is None:
            raise OrderNotFoundException()
        OrderModel.destroy(str(order.uuid))
