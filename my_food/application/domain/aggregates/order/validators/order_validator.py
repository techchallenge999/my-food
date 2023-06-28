from uuid import UUID

from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.domain.aggregates.order.interfaces.order_entity import OrderInterface
from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.product.interfaces.product_repository import ProductRepositoryInterface
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class OrderValidator(ValidatorInterface):
    def __init__(
            self,
            entity: OrderInterface,
            order_repository: OrderRepositoryInterface,
            product_repository: ProductRepositoryInterface,
        ):
        self._order = entity
        self._order_repository = order_repository
        self._product_repository = product_repository

    def validate(self):
        self._raise_if_has_unavailable_product()
        self._raise_if_has_invalid_quantity()
        self._raise_if_invalid_status()
        self._raise_if_invalid_uuid()
        self._raise_if_unavailable_uuid()

    def _raise_if_has_unavailable_product(self) -> None:
        if self._has_unavailable_product():
            raise ValueError('Pedido contém produto indisponível')

    def _raise_if_has_invalid_quantity(self) -> None:
        if self._has_invalid_product_quantity():
            raise ValueError('Pedido contém quantidade de produto inválida')

    def _raise_if_invalid_status(self) -> None:
        if self._is_invalid_status():
            raise ValueError('Pedido com status inválido')

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise ValueError('uuid inválido')

    def _raise_if_unavailable_uuid(self) -> None:
        if self._is_unavailable_uuid():
            raise ValueError('uuid indisponível')

    def _has_unavailable_product(self) -> bool:
        for item in self._order.items:
            if self._product_repository.find(str(item.product_uuid)) is None:
                return True
        return False

    def _has_invalid_product_quantity(self) -> bool:
        for item in self._order.items:
            if item.quantity <= 0:
                return True
        return False

    def _is_invalid_status(self) -> bool:
        return not isinstance(self._order.status, OrderStatus)

    def _is_invalid_uuid(self) -> bool:
        return not isinstance(self._order.uuid, UUID)

    def _is_unavailable_uuid(self) -> bool:
        return self._order_repository.find(str(self._order.uuid)) is not None
