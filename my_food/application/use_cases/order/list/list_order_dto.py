from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
)


@dataclass
class ListOrderItemOutputDto:
    comment: str
    product: ProductRepositoryDto
    quantity: int


@dataclass
class ListOrderOutputDto:
    items: list[ListOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
