from typing import List, Optional
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus
from src.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.interface_adapters.presenters.auth import EmptyUser
from src.use_cases.order.create.create_order import CreateOrderUseCase
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from src.use_cases.order.delete.delete_order import DeleteOrderUseCase
from src.use_cases.order.delete.delete_order_dto import (
    DeleteOrderInputDto,
    DeleteOrderOutputDto,
)
from src.use_cases.order.find.find_order import FindOrderUseCase
from src.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderOutputDto,
)
from src.use_cases.order.list.list_order import ListOrderUseCase
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order import UpdateOrderUseCase
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderItemInputDto,
    UpdateOrderOutputDto,
    UpdateStatusOrderInputDto,
)
from src.use_cases.user.find.find_user_dto import FindUserOutputDto


class OrderController:
    def __init__(self, repository: OrderRepositoryInterface):
        self.repository = repository

    def create_order(
        self,
        input_data,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
        current_user: FindUserOutputDto | EmptyUser,
    ) -> CreateOrderOutputDto:
        create_use_case = CreateOrderUseCase(
            self.repository, product_repository, user_repository
        )
        new_user = create_use_case.execute(
            CreateOrderInputDto(items=input_data.items, user_uuid=current_user.uuid)
        )
        return new_user

    def list_orders(
        self,
        filter_by_status: str | None = None,
        exclusive_filter_by_status: str | None = None,
    ) -> Optional[List[ListOrderOutputDto]]:
        list_use_case = ListOrderUseCase(self.repository)

        filters = {}
        if filter_by_status is None:
            filters["status"] = OrderStatus(filter_by_status).name

        exclusive_filters = {}
        if exclusive_filter_by_status is None:
            exclusive_filters["status"] = OrderStatus(exclusive_filter_by_status).name

        orders = list_use_case.execute(filters, exclusive_filters)
        return orders

    def update_order(
        self,
        input_data: UpdateOrderInputDto,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderUseCase(
            self.repository, product_repository, user_repository
        )
        orders = update_use_case.execute(input_data)
        return orders

    def retireve_order(self, order_uuid: str) -> FindOrderOutputDto:
        find_use_case = FindOrderUseCase(self.repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        return order

    def delete_order(self, order_uuid: str) -> DeleteOrderOutputDto:
        delete_use_case = DeleteOrderUseCase(self.repository)
        order = delete_use_case.execute(DeleteOrderInputDto(uuid=order_uuid))
        return order

    def update_order_status(
        self,
        order_uuid: str,
        input_data: UpdateStatusOrderInputDto,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> UpdateOrderOutputDto:
        find_use_case = FindOrderUseCase(self.repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        order = UpdateOrderInputDto(
            items=[
                UpdateOrderItemInputDto(
                    comment=item.comment,
                    product_uuid=item.product.uuid,
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=input_data.status,
            uuid=order.uuid,
        )

        update_use_case = UpdateOrderUseCase(
            self.repository, product_repository, user_repository
        )
        orders = update_use_case.execute(order)
        return orders
