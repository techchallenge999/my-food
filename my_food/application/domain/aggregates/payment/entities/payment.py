from enum import Enum
from uuid import UUID, uuid4

from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.payment.interfaces.payment_entity import PaymentInterface
from my_food.application.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from my_food.application.domain.aggregates.payment.validators.payment_validator import PaymentValidator
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class PaymentStatus(Enum):
    PAID = 'pendente'
    PENDING = 'pago'


class Payment(PaymentInterface):
    def __init__(
        self,
        order_uuid: UUID,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
        status: PaymentStatus = PaymentStatus.PENDING,
        uuid: UUID = uuid4(),
    ):
        self._order_uuid = order_uuid
        self._status = status
        self._uuid = uuid
        self._validator = PaymentValidator(self, payment_repository, order_repository)
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
