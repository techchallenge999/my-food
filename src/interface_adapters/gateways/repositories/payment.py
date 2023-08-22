from abc import abstractmethod
from dataclasses import dataclass

from src.domain.aggregates.payment.interfaces.payment_entity import PaymentStatus
from src.domain.shared.interfaces.repository import RepositoryInterface
from src.use_cases.payment.create.create_payment_dto import CreatePaymentOutputDto
from src.use_cases.payment.update.update_payment_dto import UpdatePaymentOutputDto


@dataclass
class PaymentRepositoryDto:
    order_uuid: str
    status: PaymentStatus
    uuid: str


class PaymentRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, new_payment_dto: CreatePaymentOutputDto) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> PaymentRepositoryDto:
        pass

    @abstractmethod
    def find_by_order(self, order_uuid: str) -> PaymentRepositoryDto:
        pass

    @abstractmethod
    def list(self) -> list[PaymentRepositoryDto]:
        pass

    @abstractmethod
    def update(self, updated_payment_dto: UpdatePaymentOutputDto) -> None:
        pass
