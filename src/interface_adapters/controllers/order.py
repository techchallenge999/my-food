from src.infrastructure.fast_api.utils.auth import EmptyUser
from src.interface_adapters.gateways.order_parser import CreateOrderParser
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
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
from src.use_cases.order.update.update_order import (
    UpdateOrderItemsUseCase,
    UpdateOrderStatusUseCase,
)
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderOutputDto,
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

    def list_orders(self) -> list[ListOrderOutputDto]:
        return ListOrderUseCase(self.repository).execute()

    def retireve_order(self, order_uuid: str) -> FindOrderOutputDto:
        find_use_case = FindOrderUseCase(self.repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        return order

    def update_order_items(
        self,
        order_uuid: str,
        input_data: UpdateOrderItemsInputDto,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderItemsUseCase(
            self.repository, product_repository, user_repository
        )
        order = update_use_case.execute(order_uuid, input_data)
        return order

    def progress_order_status(
        self,
        order_uuid: str,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderStatusUseCase(
            self.repository, product_repository, user_repository
        )
        order = update_use_case.progress(order_uuid)
        return order

    def cancel_order(
        self,
        order_uuid: str,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderStatusUseCase(
            self.repository, product_repository, user_repository
        )
        order = update_use_case.cancel(order_uuid)
        return order

    def delete_order(self, order_uuid: str) -> DeleteOrderOutputDto:
        delete_use_case = DeleteOrderUseCase(self.repository)
        order = delete_use_case.execute(DeleteOrderInputDto(uuid=order_uuid))
        return order
