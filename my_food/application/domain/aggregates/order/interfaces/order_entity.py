from abc import ABC, abstractmethod
from uuid import UUID
from my_food.application.domain.aggregates.order.entities.order import OrderStatusCategory
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class OrderItemInterface(ABC):
    _comment: str
    _product_uuid: UUID
    _quantity: int

    @property
    @abstractmethod
    def comment(self) -> str:
        pass

    @property
    @abstractmethod
    def product_uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass


class OrderInterface(ABC):
    _items: list[OrderItemInterface]
    _status: OrderStatusCategory
    _total_amount: str
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def items(self) -> list[OrderItemInterface]:
        pass

    @property
    @abstractmethod
    def status(self) -> OrderStatusCategory:
        pass

    @property
    @abstractmethod
    def total_amount(self) -> str:
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
