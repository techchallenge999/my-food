from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.value_objects.order_status import OrderStatus


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
    created_at: datetime
    updated_at: datetime
