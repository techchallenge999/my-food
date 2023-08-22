from dataclasses import dataclass
from src.domain.aggregates.order.entities.order import OrderStatus
from src.use_cases.product.find.find_product_dto import (
    FindProductOutputDto,
)


@dataclass
class UpdateOrderItemInputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class UpdateOrderItemOutputDto:
    comment: str
    product: FindProductOutputDto
    quantity: int


@dataclass
class UpdateOrderItemsInputDto:
    items: list[UpdateOrderItemInputDto]


@dataclass
class UpdateOrderOutputDto:
    items: list[UpdateOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
