from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from my_food.application.domain.aggregates.order.interfaces.order_entity import OrderInterface, OrderItemInterface
from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.order.validators.order_validator import OrderValidator
from my_food.application.domain.aggregates.product.interfaces.product_repository import ProductRepositoryInterface
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class OrderStatus(Enum):
    RECEIVED = 'recebido'
    PREPARING = 'preparando'
    READY = 'pronto'
    WITHDRAWN = 'retirado'


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


class Order(OrderInterface):
    def __init__(
        self,
        items: list[OrderItemInterface],
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        status: OrderStatus = OrderStatus.RECEIVED,
        uuid: UUID = uuid4(),
    ):
        self._items = items
        self._status = status
        self._total_amount = self._get_total_amount(product_repository)
        self._uuid = uuid
        self._validator = OrderValidator(self, order_repository, product_repository)
        self.validator.validate()

    @property
    def items(self) -> list[OrderItemInterface]:
        return self._items

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def total_amount(self) -> str:
        return self._total_amount

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator

    def _get_total_amount(self, product_repository: ProductRepositoryInterface) -> str:
        total_amount = Decimal('0')
        for item in self.items:
            product = product_repository.find(item.product_uuid)
            total_amount += Decimal(str(item.quantity)) * Decimal(product.price)
        return str(total_amount)
