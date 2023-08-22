from dataclasses import asdict
from uuid import UUID

from src.domain.aggregates.order.entities.order import Order
from src.domain.aggregates.order.interfaces.order_entity import (
    OrderItemInterface,
    OrderStatus,
)
from src.domain.aggregates.order.value_objects.order_item import OrderItem
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryDto,
    OrderRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderItemOutputDto,
    UpdateOrderOutputDto,
)
from src.use_cases.product.find.find_product_dto import FindProductOutputDto


class BaseUpdateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository

    def base_execute(
        self,
        order: OrderRepositoryDto,
        items: list[OrderItemInterface],
        status: OrderStatus,
    ) -> UpdateOrderOutputDto:
        updated_order = Order(
            items=items,
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            status=status,
            user_uuid=UUID(order.user_uuid)
            if isinstance(order.user_uuid, str)
            else None,
            uuid=UUID(order.uuid),
        )
        updated_order_dto = UpdateOrderOutputDto(
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
        self._order_repository.update(updated_order_dto)
        return updated_order_dto

    def find_order(self, order_uuid: str) -> OrderRepositoryDto:
        order = self._order_repository.find(order_uuid)
        if order is None:
            raise OrderNotFoundException()
        return order


class UpdateOrderItemsUseCase(BaseUpdateOrderUseCase):
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        super().__init__(order_repository, product_repository, user_repository)

    def execute(
        self, order_uuid: str, input_data: UpdateOrderItemsInputDto
    ) -> UpdateOrderOutputDto:
        order = self.find_order(order_uuid)
        items = [
            OrderItem(
                comment=item.comment,
                product_uuid=UUID(item.product_uuid),
                quantity=item.quantity,
            )
            for item in input_data.items
        ]
        status = order.status
        return super().base_execute(order, items, status)


class UpdateOrderStatusUseCase(BaseUpdateOrderUseCase):
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        super().__init__(order_repository, product_repository, user_repository)

    def progress(self, order_uuid: str) -> UpdateOrderOutputDto:
        order = self.find_order(order_uuid)
        items = [
            OrderItem(
                comment=item.comment,
                product_uuid=UUID(item.product.uuid),
                quantity=item.quantity,
            )
            for item in order.items
        ]
        status = order.status.next()
        return super().base_execute(order, items, status)

    def cancel(self, order_uuid: str) -> UpdateOrderOutputDto:
        order = self.find_order(order_uuid)
        items = [
            OrderItem(
                comment=item.comment,
                product_uuid=UUID(item.product.uuid),
                quantity=item.quantity,
            )
            for item in order.items
        ]
        status = OrderStatus.CANCELED
        return super().base_execute(order, items, status)
