from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.value_objects.order_status import OrderStatus


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
    created_at: datetime
    updated_at: datetime
    uuid: str
