from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from uuid import UUID

from src.domain.shared.interfaces.validator import ValidatorInterface


class OrderStatus(Enum):
    PENDING_PAYMENT = "pagamento pendente"
    CANCELED = "cancelado"
    RECEIVED = "recebido"
    PREPARING = "preparando"
    READY = "pronto"
    WITHDRAWN = "retirado"


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
    _status: OrderStatus
    _total_amount: str
    _user_uuid: UUID | None
    _uuid: UUID
    _created_at: datetime
    _updated_at: datetime
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
    def user_uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
