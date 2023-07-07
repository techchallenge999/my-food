from uuid import UUID
from my_food.application.domain.aggregates.order.interfaces.order_entity import OrderItemInterface


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

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def product_uuid(self) -> str:
        return str(self._product_uuid)

    @property
    def quantity(self) -> int:
        return self._quantity
