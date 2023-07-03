from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from my_food.application.domain.aggregates.payment.entities.payment import PaymentStatus
from my_food.application.domain.aggregates.payment.interfaces.payment_entity import PaymentInterface
from my_food.application.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class PaymentRepositoryDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str


class PaymentRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: PaymentInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[PaymentRepositoryDto]:
        pass

    @abstractmethod
    def list(self) -> Optional[List[PaymentRepositoryDto]]:
        pass

    @abstractmethod
    def update(self, entity: PaymentInterface) -> None:
        pass
