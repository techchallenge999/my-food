from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.interfaces.repository import RepositoryInterface
from src.interface_adapters.gateways.repositories.product import ProductRepositoryDto
from src.use_cases.order.create.create_order_dto import CreateOrderOutputDto
from src.use_cases.order.update.update_order_dto import UpdateOrderOutputDto


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
    def create(self, create_order_dto: CreateOrderOutputDto) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> OrderRepositoryDto | None:
        pass

    @abstractmethod
    def list(
        self, filters: dict = {}, exclusive_filters: dict = {}
    ) -> list[OrderRepositoryDto]:
        pass

    @abstractmethod
    def update(self, update_order_dto: UpdateOrderOutputDto) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
