from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.shared.interfaces.validator import ValidatorInterface


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

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
