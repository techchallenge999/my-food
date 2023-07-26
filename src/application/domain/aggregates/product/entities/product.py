from uuid import UUID, uuid4

from src.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
    ProductCategory,
)
from src.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.application.domain.aggregates.product.validators.product_validator import (
    ProductValidator,
)
from src.application.domain.shared.interfaces.validator import ValidatorInterface


class Product(ProductInterface):
    def __init__(
        self,
        name: str,
        category: ProductCategory,
        price: float,
        description: str,
        image: bytes,
        repository: ProductRepositoryInterface,
        is_active: bool = False,
        uuid: UUID = None,
    ):
        self._name = name
        self._category = category
        self._price = price
        self._description = description
        self._image = image
        self._uuid = uuid or uuid4()
        self._is_active = is_active
        self._validator = ProductValidator(self, repository)
        self.validator.validate()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def category(self) -> ProductCategory:
        return self._category

    @category.setter
    def category(self, value: ProductCategory):
        self._category = value

    @property
    def price(self) -> str:
        return self._price

    @price.setter
    def price(self, value: str):
        self._price = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def image(self) -> bytes:
        return self._image

    @image.setter
    def image(self, value: bytes):
        self._image = value

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = value

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator
