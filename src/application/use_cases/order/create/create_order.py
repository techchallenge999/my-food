from dataclasses import asdict
from uuid import UUID

from src.application.domain.aggregates.order.entities.order import Order
from src.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from src.application.domain.aggregates.order.value_objects.order_item import OrderItem
from src.application.domain.aggregates.product.interfaces.product_repository import ProductRepositoryInterface
from src.application.domain.aggregates.user.interfaces.user_repository import UserRepositoryInterface
from src.application.use_cases.order.create.create_order_dto import CreateOrderInputDto, CreateOrderItemOutputDto, CreateOrderOutputDto
from src.application.use_cases.product.find.find_product_dto import FindProductOutputDto


class CreateOrderUseCase:
    def __init__(
            self,
            order_repository: OrderRepositoryInterface,
            product_repository: ProductRepositoryInterface,
            user_repository: UserRepositoryInterface,
        ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository


    def execute(self, input_data: CreateOrderInputDto) -> CreateOrderOutputDto:
        new_order = Order(
            items=[
                OrderItem(
                    comment=item.comment,
                    product_uuid=UUID(item.product_uuid),
                    quantity=item.quantity,
                )
                for item in input_data.items
            ],
            order_repository=self._order_repository,
            product_repository=self._product_repository,
            user_repository=self._user_repository,
            user_uuid=UUID(input_data.user_uuid) if isinstance(input_data.user_uuid, str) else None,
        )

        self._order_repository.create(entity=new_order)

        return CreateOrderOutputDto(
            items=[
                CreateOrderItemOutputDto(
                    comment=new_item.comment,
                    product=FindProductOutputDto(**asdict(self._product_repository.find(new_item.product_uuid))),
                    quantity=new_item.quantity,
                )
                for new_item in new_order.items
            ],
            status=new_order.status,
            total_amount=new_order.total_amount,
            user_uuid=new_order.user_uuid,
            uuid=new_order.uuid,
        )
