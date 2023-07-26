from uuid import UUID, uuid4

from src.application.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from src.application.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentInterface,
    PaymentStatus,
)
from src.application.domain.aggregates.payment.interfaces.payment_repository import (
    PaymentRepositoryInterface,
)
from src.application.domain.aggregates.payment.validators.payment_validator import (
    PaymentValidator,
)
from src.application.domain.shared.interfaces.validator import ValidatorInterface


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
