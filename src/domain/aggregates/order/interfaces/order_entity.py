from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from uuid import UUID

from src.domain.shared.exceptions.order import OrderStatusProgressionNotAllowedException
from src.domain.shared.interfaces.validator import ValidatorInterface


class OrderStatus(Enum):
    CANCELED = "cancelado"
    PENDING_PAYMENT = "pagamento pendente"
    RECEIVED = "recebido"
    PREPARING = "preparando"
    READY = "pronto"
    WITHDRAWN = "retirado"

    def next(self):
        members = list(self.__class__)
        current_index = members.index(self)
        if members[current_index] in {members[0], members[-1]}:
            raise OrderStatusProgressionNotAllowedException()
        return members[current_index + 1]


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
