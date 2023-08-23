from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.entities.order import OrderStatus
from src.use_cases.product.find.find_product_dto import FindProductOutputDto


@dataclass
class FindOrderItemOutputDto:
    comment: str
    product: FindProductOutputDto
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
