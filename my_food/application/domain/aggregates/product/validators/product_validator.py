from uuid import UUID

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.base import (
    InvalidUUIDException,
)
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class ProductValidator(ValidatorInterface):
    def __init__(
        self, entity: ProductInterface, repository: ProductRepositoryInterface
    ):
        self._product = entity
        self._repository = repository

    def validate(self):
        self._raise_if_invalid_uuid()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _is_invalid_uuid(self) -> bool:
        return isinstance(self._product.uuid, UUID)
