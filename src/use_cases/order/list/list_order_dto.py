from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.use_cases.product.list.list_product_dto import ListProductOutputDto


@dataclass
class ListOrderItemOutputDto:
    comment: str
    product: ListProductOutputDto
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
