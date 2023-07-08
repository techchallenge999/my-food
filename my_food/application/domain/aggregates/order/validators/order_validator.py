from uuid import UUID

from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.domain.aggregates.order.interfaces.order_entity import (
    OrderInterface,
)
from my_food.application.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.base import (
    InvalidUUIDException,
)
from my_food.application.domain.shared.errors.exceptions.order import (
    InvalidOrderStatusException,
)
from my_food.application.domain.shared.errors.exceptions.product import (
    InvalidProductQuantityException,
    UnavailableProductException,
)
from my_food.application.domain.shared.errors.exceptions.user import (
    UserNotFoundException,
)
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class OrderValidator(ValidatorInterface):
    def __init__(
        self,
        entity: OrderInterface,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._order = entity
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository

    def validate(self):
        self._raise_if_has_unavailable_product()
        self._raise_if_has_invalid_quantity()
        self._raise_if_invalid_order_status()
        self._raise_if_invalid_uuid()
        self._raise_if_nonexistent_user()

    def _raise_if_has_unavailable_product(self) -> None:
        if self._has_unavailable_product():
            raise UnavailableProductException()

    def _raise_if_has_invalid_quantity(self) -> None:
        if self._has_invalid_product_quantity():
            raise InvalidProductQuantityException()

    def _raise_if_invalid_order_status(self) -> None:
        if self._is_invalid_order_status():
            raise InvalidOrderStatusException()

    def _raise_if_nonexistent_user(self) -> None:
        if self._is_nonexistent_user():
            raise UserNotFoundException()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _is_nonexistent_user(self) -> bool:
        return (
            self._order.user_uuid is not None
            and self._user_repository.find(self._order.user_uuid) is None
        )

    def _has_unavailable_product(self) -> bool:
        for item in self._order.items:
            if self._product_repository.find(item.product_uuid) is None:
                return True
        return False

    def _has_invalid_product_quantity(self) -> bool:
        for item in self._order.items:
            if item.quantity <= 0:
                return True
        return False

    def _is_invalid_order_status(self) -> bool:
        return not isinstance(self._order.status, OrderStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._order.uuid), UUID)
        except ValueError:
            return True
