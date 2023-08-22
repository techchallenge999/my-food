from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
    OrderStatus,
)
from src.domain.shared.interfaces.repository import RepositoryInterface
from src.interface_adapters.gateways.repositories.product import ProductRepositoryDto


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
    def find(self, uuid: str) -> OrderRepositoryDto | None:
        pass

    @abstractmethod
    def list(
        self, filters: dict | None = None, exclusive_filters: dict | None = None
    ) -> list[OrderRepositoryDto]:
        pass

    @abstractmethod
    def update(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
