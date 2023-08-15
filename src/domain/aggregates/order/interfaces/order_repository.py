from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
    OrderStatus,
)
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
)
from src.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class OrderItemRepositoryOutputDto:
    comment: str
    product: ProductRepositoryDto
    quantity: int


@dataclass
class OrderRepositoryOutputDto:
    items: list[OrderItemRepositoryOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    created_at: datetime
    updated_at: datetime
    uuid: str


class OrderRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[OrderRepositoryOutputDto]:
        pass

    @abstractmethod
    def list(
        self, filters: dict, exclusive_filters: dict
    ) -> Optional[List[OrderRepositoryOutputDto]]:
        pass

    @abstractmethod
    def update(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
