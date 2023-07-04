from uuid import UUID

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.base import InvalidUUIDException, UnavailableUUIDException
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class ProductValidator(ValidatorInterface):
    def __init__(
        self, entity: ProductInterface, repository: ProductRepositoryInterface
    ):
        self._product = entity
        self._repository = repository

    def validate(self):
        self._raise_if_invalid_uuid()
        self._raise_if_unavailable_uuid()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _raise_if_unavailable_uuid(self) -> None:
        if self._is_unavailable_uuid():
            raise UnavailableUUIDException()

    def _is_invalid_uuid(self) -> bool:
        return isinstance(self._product.uuid, UUID)

    def _is_unavailable_uuid(self) -> bool:
        return self._repository.find(str(self._product.uuid)) is not None
