from uuid import UUID, uuid4

from src.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentInterface,
    PaymentStatus,
)
from src.domain.aggregates.payment.validators.payment_validator import PaymentValidator
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.domain.shared.interfaces.validator import ValidatorInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface


class Payment(PaymentInterface):
    def __init__(
        self,
        order_uuid: UUID,
        order_repository: OrderRepositoryInterface,
        status: PaymentStatus = PaymentStatus.PENDING,
        uuid: UUID = uuid4(),
    ):
        self._order_uuid = order_uuid
        self._status = status
        self._uuid = uuid
        self._order_repository = order_repository
        self._validator = PaymentValidator(self, order_repository)
        self.validator.validate()

    @property
    def order_uuid(self) -> str:
        return str(self._order_uuid)

    @property
    def status(self) -> PaymentStatus:
        return self._status

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator

    @property
    def total(self) -> str:
        order = self._order_repository.find(self.order_uuid)
        if order is None:
            raise OrderNotFoundException()
        return order.total_amount
