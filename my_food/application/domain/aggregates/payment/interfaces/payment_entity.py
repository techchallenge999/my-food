from abc import ABC, abstractmethod
from uuid import UUID

from my_food.application.domain.aggregates.payment.entities.payment import PaymentStatus
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


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
