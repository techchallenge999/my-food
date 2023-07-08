from dataclasses import dataclass
from datetime import datetime
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
    created_at: datetime
    updated_at: datetime
    uuid: str
