from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
)


@dataclass
class FindOrderItemOutputDto:
    comment: str
    product: ProductRepositoryDto
    quantity: int


@dataclass
class FindOrderInputDto:
    uuid: str


@dataclass
class FindOrderOutputDto:
    items: list[FindOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
