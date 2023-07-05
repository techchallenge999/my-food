from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from my_food.application.domain.aggregates.order.entities.order import OrderStatus

from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
)
from my_food.application.domain.shared.interfaces.repository import RepositoryInterface


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
    uuid: str


class OrderRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[OrderRepositoryDto]:
        pass

    @abstractmethod
    def list(self, filters: dict) -> Optional[List[OrderRepositoryDto]]:
        pass

    @abstractmethod
    def update(self, entity: OrderInterface) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
