from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus


@dataclass
class FindOrderItemOutputDto:
    comment: str
    product_uuid: str
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
