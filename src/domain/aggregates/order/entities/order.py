from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
    OrderItemInterface,
    OrderStatus,
)
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.aggregates.order.validators.order_validator import (
    OrderValidator,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


class Order(OrderInterface):
    def __init__(
        self,
        items: list[OrderItemInterface],
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
        status: OrderStatus = OrderStatus.RECEIVED,
        user_uuid: UUID | None = None,
        uuid: UUID = uuid4(),
        created_at: datetime = datetime.now(),
        updated_at: datetime | None = None,
    ):
        self._items = items
        self._status = status
        self._total_amount = self._get_total_amount(product_repository)
        self._user_uuid = user_uuid
        self._uuid = uuid
        self.created_at = created_at
        self.updated_at = updated_at
        self._validator = OrderValidator(
            self, order_repository, product_repository, user_repository
        )
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
    def user_uuid(self) -> str | None:
        if isinstance(self._user_uuid, UUID):
            return str(self._user_uuid)
        return None

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator

    def _get_total_amount(self, product_repository: ProductRepositoryInterface) -> str:
        total_amount = Decimal("0")
        for item in self.items:
            product = product_repository.find(item.product_uuid)
            total_amount += Decimal(str(item.quantity)) * Decimal(product.price)
        return str(total_amount)
