from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class PaymentStatus(Enum):
    PENDING = "pendente"
    PAID = "pago"
    REFUSED = "recusado"


class PaymentInterface(ABC):
    _order_uuid: UUID
    _status: PaymentStatus
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def order_uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def status(self) -> PaymentStatus:
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
