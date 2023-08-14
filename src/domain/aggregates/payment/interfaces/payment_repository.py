from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from src.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentInterface,
    PaymentStatus,
)
from src.domain.shared.interfaces.repository import RepositoryInterface


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
