from uuid import UUID

from src.domain.aggregates.order.interfaces.entities import OrderItemInterface
from src.domain.aggregates.order.validators.order_item_validator import (
    OrderItemValidator,
)


class OrderItem(OrderItemInterface):
    def __init__(
        self,
        comment: str,
        product_uuid: UUID,
        quantity: int,
    ):
        self._comment = comment
        self._product_uuid = product_uuid
        self._quantity = quantity
        self._validator = OrderItemValidator(self)
        self.validator.validate()

    @property
    def comment(self):
        return self._comment

    @property
    def product_uuid(self):
        return str(self._product_uuid)

    @property
    def quantity(self):
        return self._quantity

    @property
    def validator(self):
        return self._validator
