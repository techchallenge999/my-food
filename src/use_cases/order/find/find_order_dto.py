from dataclasses import dataclass
from datetime import datetime
from src.domain.aggregates.order.entities.order import OrderStatus
from src.interface_adapters.gateways.repositories.product import (
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
