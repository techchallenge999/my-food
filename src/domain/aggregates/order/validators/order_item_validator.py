from src.domain.aggregates.order.interfaces.value_objects import OrderItemInterface
from src.domain.shared.exceptions.product import InvalidProductQuantityException
from src.domain.shared.interfaces.validator import ValidatorInterface


class OrderItemValidator(ValidatorInterface):
    def __init__(
        self,
        domain_object: OrderItemInterface,
    ):
        self._order_item = domain_object

    def validate(self):
        self._raise_if_has_invalid_quantity()

    def _raise_if_has_invalid_quantity(self) -> None:
        if self._has_invalid_quantity():
            raise InvalidProductQuantityException()

    def _has_invalid_quantity(self) -> bool:
        return self._order_item.quantity <= 0
