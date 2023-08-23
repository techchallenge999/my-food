from uuid import UUID

from src.domain.aggregates.order.interfaces.entities import OrderInterface
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.exceptions.base import InvalidUUIDException
from src.domain.shared.exceptions.order import InvalidOrderStatusException
from src.domain.shared.exceptions.product import UnavailableProductException
from src.domain.shared.exceptions.user import UserNotFoundException
from src.domain.shared.interfaces.validator import ValidatorInterface
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface


class OrderValidator(ValidatorInterface):
    def __init__(
        self,
        domain_object: OrderInterface,
        order_repository: OrderRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._order = domain_object
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._user_repository = user_repository

    def validate(self):
        self._raise_if_has_unavailable_product()
        self._raise_if_invalid_order_status()
        self._raise_if_invalid_uuid()
        self._raise_if_nonexistent_user()

    def _raise_if_has_unavailable_product(self) -> None:
        if self._has_unavailable_product():
            raise UnavailableProductException()

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

    def _is_invalid_order_status(self) -> bool:
        return not isinstance(self._order.status, OrderStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._order.uuid), UUID)
        except ValueError:
            return True
