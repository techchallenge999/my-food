from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.use_cases.product.delete.delete_product_dto import (
    DeleteProductOutputDto,
)


@dataclass
class DeleteOrderItemOutputDto:
    comment: str
    product: DeleteProductOutputDto
    quantity: int


@dataclass
class DeleteOrderInputDto:
    uuid: str


@dataclass
class DeleteOrderOutputDto:
    items: list[DeleteOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
