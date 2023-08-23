from uuid import UUID

from src.domain.aggregates.order.entities.order import Order
from src.domain.aggregates.order.interfaces.order import OrderInterface
from src.domain.aggregates.order.value_objects.order_item import OrderItem
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.order.find.find_order import FindOrderUseCase
from src.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderOutputDto,
)
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderItemOutputDto,
    UpdateOrderOutputDto,
)


class UpdateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
        find_order_use_case: FindOrderUseCase,
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository
        self._find_order_use_case = find_order_use_case

    def update_order_items(
        self, order_uuid: str, new_order_items: UpdateOrderItemsInputDto
    ) -> UpdateOrderOutputDto:
        find_order_dto = self._find_order_use_case.execute(
            FindOrderInputDto(order_uuid)
        )
        order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in new_order_items.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            status=find_order_dto.status,
            user_uuid=self._get_user_uuid(find_order_dto),
            uuid=UUID(find_order_dto.uuid),
        )
        return self._execute(order)

    def progress_status(self, order_uuid: str) -> UpdateOrderOutputDto:
        find_order_dto = self._find_order_use_case.execute(
            FindOrderInputDto(order_uuid)
        )
        order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product.uuid),
                    quantity=item.quantity,
                )
                for item in find_order_dto.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            status=find_order_dto.status.next(),
            user_uuid=self._get_user_uuid(find_order_dto),
            uuid=UUID(find_order_dto.uuid),
        )
        return self._execute(order)

    def cancel(self, order_uuid: str) -> UpdateOrderOutputDto:
        find_order_dto = self._find_order_use_case.execute(
            FindOrderInputDto(order_uuid)
        )
        order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product.uuid),
                    quantity=item.quantity,
                )
                for item in find_order_dto.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            status=OrderStatus.CANCELED,
            user_uuid=self._get_user_uuid(find_order_dto),
            uuid=UUID(find_order_dto.uuid),
        )
        return self._execute(order)

    def _execute(self, order: OrderInterface) -> UpdateOrderOutputDto:
        update_order_dto = UpdateOrderOutputDto(
            items=[
                UpdateOrderItemOutputDto(
                    comment=item.comment,
                    product_uuid=item.product_uuid,
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            user_uuid=order.user_uuid,
            uuid=order.uuid,
        )
        self._order_repository.update(update_order_dto)
        return update_order_dto

    def _get_user_uuid(self, find_order_dto: FindOrderOutputDto) -> UUID | None:
        return UUID(find_order_dto.user_uuid) if find_order_dto.user_uuid else None
