from typing import List, Optional
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.interface_adapters.gateways.auth import EmptyUser
from src.interface_adapters.gateways.order import CreateOrderParser
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
from src.use_cases.order.list.list_order import (
    ListAllButWithdrawOrdersUseCase,
    ListOrderUseCase,
)
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
        input_data: CreateOrderInputDto,
        create_order_parser: CreateOrderParser,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
        current_user: FindUserOutputDto | EmptyUser,
    ) -> CreateOrderOutputDto:
        create_use_case = CreateOrderUseCase(
            self.repository, product_repository, user_repository
        )
        new_user = create_use_case.execute(
            create_order_parser.get_dto(input_data, current_user)
        )
        return new_user

    def list_orders(
        self,
        status: str | None = None,
    ) -> Optional[List[ListOrderOutputDto]]:
        list_use_case = ListOrderUseCase(self.repository)

        filters = {}
        if status is not None:
            filters["status"] = OrderStatus(status).name

        orders = list_use_case.execute(filters)
        return orders

    def list_all_but_withdrawn(self) -> Optional[List[ListOrderOutputDto]]:
        return ListAllButWithdrawOrdersUseCase(self.repository).execute()

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
