from dataclasses import dataclass
from datetime import datetime
from src.domain.aggregates.order.entities.order import OrderStatus
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryDto,
)


@dataclass
class ListOrderItemOutputDto:
    comment: str
    product: ProductRepositoryDto
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
