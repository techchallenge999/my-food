from uuid import UUID

from sqlalchemy import case, select
from sqlalchemy.orm import subqueryload

from src.domain.aggregates.order.interfaces.order_entity import OrderStatus
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.models.order import OrderItemModel, OrderModel
from src.interface_adapters.gateways.repositories.order import (
    OrderItemRepositoryDto,
    OrderRepositoryDto,
    OrderRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import ProductRepositoryDto
from src.use_cases.order.create.create_order_dto import CreateOrderOutputDto
from src.use_cases.order.update.update_order_dto import UpdateOrderOutputDto


class OrderRepository(OrderRepositoryInterface):
    def create(self, new_order_dto: CreateOrderOutputDto) -> None:
        new_order = OrderModel(
            status=OrderStatus.RECEIVED,
            total_amount=new_order_dto.total_amount,
            uuid=new_order_dto.uuid,
            user_uuid=new_order_dto.user_uuid,
        )
        new_order.create()
        for item in new_order_dto.items:
            new_order_item = OrderItemModel(
                comment=item.comment,
                order_uuid=new_order_dto.uuid,
                product_uuid=item.product.uuid,
                quantity=item.quantity,
            )
            new_order_item.create()

    def find(self, uuid: str) -> OrderRepositoryDto | None:
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

    def list(
        self,
        filters: dict = {},
        exclusive_filters: dict = {},
    ) -> list[OrderRepositoryDto]:
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

    def update(self, updated_order_dto: UpdateOrderOutputDto) -> None:
        order = OrderModel.retrieve(updated_order_dto.uuid)
        if order:
            for item in order.items:
                item.self_destroy()
            for item in updated_order_dto.items:
                OrderItemModel(
                    comment=item.comment,
                    order_uuid=order.uuid,
                    product_uuid=item.product.uuid,
                    quantity=item.quantity,
                ).create()

            OrderModel.update(
                {
                    "items": updated_order_dto.items,
                    "status": updated_order_dto.status,
                    "total_amount": updated_order_dto.total_amount,
                    "uuid": updated_order_dto.uuid,
                    "id": order.id,
                }
            )

    def delete(self, uuid: str) -> OrderRepositoryDto | None:
        order = OrderModel.retrieve(uuid)
        if order is None:
            raise OrderNotFoundException()
        OrderModel.destroy(str(order.uuid))
