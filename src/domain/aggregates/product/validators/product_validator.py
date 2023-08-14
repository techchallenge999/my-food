from uuid import UUID

from src.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
)
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.shared.exceptions.base import (
    InvalidUUIDException,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


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
        try:
            return not isinstance(UUID(self._product.uuid), UUID)
        except ValueError:
            return True
