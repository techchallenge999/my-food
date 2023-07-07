from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus


@dataclass
class ListOrderItemOutputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class ListOrderOutputDto:
    items: list[ListOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
