from dataclasses import asdict
from uuid import UUID

from my_food.application.domain.aggregates.order.entities.order import Order, OrderItem
from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.product.interfaces.product_repository import ProductRepositoryInterface
from my_food.application.use_cases.order.create.create_order_dto import CreateOrderInputDto, CreateOrderItemOutputDto, CreateOrderOutputDto
from my_food.application.use_cases.product.find.find_product_dto import FindProductOutputDto


class CreateOrderUseCase:
    def __init__(
            self,
            order_repository: OrderRepositoryInterface,
            product_repository: ProductRepositoryInterface,
        ):
        self._order_repository = order_repository
        self._product_repository = product_repository

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
            uuid=new_order.uuid,
        )
