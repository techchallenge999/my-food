from dataclasses import dataclass
from src.domain.aggregates.order.entities.order import OrderStatus


@dataclass
class DeleteOrderItemOutputDto:
    comment: str
    product_uuid: str
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
