from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
    OrderStatus,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryDto,
)
from src.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class OrderItemRepositoryDto:
    comment: str
    product: ProductRepositoryDto
    quantity: int


@dataclass
class OrderRepositoryDto:
    items: list[OrderItemRepositoryDto]
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
    def find(self, uuid: str) -> Optional[OrderRepositoryDto]:
        pass

    @abstractmethod
    def list(
        self, filters: dict | None = None, exclusive_filters: dict | None = None
    ) -> Optional[List[OrderRepositoryDto]]:
        pass

    @abstractmethod
    def update(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
