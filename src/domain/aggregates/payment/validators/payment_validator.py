from uuid import UUID

from src.domain.aggregates.payment.entities.payment import PaymentStatus
from src.domain.aggregates.payment.interfaces.payment_entity import (
    PaymentInterface,
)
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


class PaymentValidator(ValidatorInterface):
    def __init__(
        self,
        entity: PaymentInterface,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface,
    ):
        self._payment = entity
        self._payment_repository = payment_repository
        self._order_repository = order_repository

    def validate(self):
        self._raise_if_nonexistent_order()
        self._raise_if_invalid_payment_status()
        self._raise_if_invalid_uuid()
        self._raise_if_unavailable_uuid()

    def _raise_if_nonexistent_order(self) -> None:
        if self._is_nonexistent_order():
            raise ValueError("Pedido inválido")

    def _raise_if_invalid_payment_status(self) -> None:
        if self._is_invalid_payment_status():
            raise ValueError("Pagamento com status inválido")

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise ValueError("uuid inválido")

    def _raise_if_unavailable_uuid(self) -> None:
        if self._is_unavailable_uuid():
            raise ValueError("uuid indisponível")

    def _is_nonexistent_order(self) -> bool:
        return self._order_repository.find(self._payment.order_uuid) is None

    def _is_invalid_payment_status(self) -> bool:
        return not isinstance(self._payment.status, PaymentStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._payment.uuid), UUID)
        except ValueError:
            return True

    def _is_unavailable_uuid(self) -> bool:
        return self._payment_repository.find(self._payment.uuid) is not None
