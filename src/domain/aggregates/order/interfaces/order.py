from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.order.interfaces.order_item import OrderItemInterface
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.interfaces.validator import ValidatorInterface


class OrderInterface(ABC):
    _items: list[OrderItemInterface]
    _status: OrderStatus
    _total_amount: str
    _user_uuid: UUID | None
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def items(self) -> list[OrderItemInterface]:
        pass

    @property
    @abstractmethod
    def status(self) -> OrderStatus:
        pass

    @property
    @abstractmethod
    def total_amount(self) -> str:
        pass

    @property
    @abstractmethod
    def user_uuid(self) -> str | None:
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
