from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.payment.value_objects.payment_status import PaymentStatus
from src.domain.shared.interfaces.validator import ValidatorInterface


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

    @property
    @abstractmethod
    def total(self) -> str:
        pass
