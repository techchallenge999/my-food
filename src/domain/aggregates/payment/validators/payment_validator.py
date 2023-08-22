from uuid import UUID
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus

from src.domain.aggregates.payment.entities.payment import PaymentStatus
from src.domain.aggregates.payment.interfaces.payment_entity import PaymentInterface
from src.domain.shared.interfaces.validator import ValidatorInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface


class PaymentValidator(ValidatorInterface):
    def __init__(
        self,
        entity: PaymentInterface,
        order_repository: OrderRepositoryInterface,
    ):
        self._payment = entity
        self._order_repository = order_repository

    def validate(self):
        self._raise_if_invalid_order()
        self._raise_if_invalid_payment_status()
        self._raise_if_invalid_uuid()

    def _raise_if_invalid_order(self) -> None:
        if self._is_invalid_order():
            raise ValueError("Pedido inválido")

    def _raise_if_invalid_payment_status(self) -> None:
        if self._is_invalid_payment_status():
            raise ValueError("Pagamento com status inválido")

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise ValueError("uuid inválido")

    def _is_invalid_order(self) -> bool:
        order = self._order_repository.find(self._payment.order_uuid)
        return order is None or order.status != OrderStatus.PENDING_PAYMENT

    def _is_invalid_payment_status(self) -> bool:
        return not isinstance(self._payment.status, PaymentStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._payment.uuid), UUID)
        except ValueError:
            return True
