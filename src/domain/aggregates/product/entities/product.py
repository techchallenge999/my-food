from uuid import UUID, uuid4

from src.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
    ProductCategory,
)
from src.domain.aggregates.product.validators.product_validator import ProductValidator
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)


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
        uuid: UUID = uuid4(),
    ):
        self._name = name
        self._category = category
        self._price = price
        self._description = description
        self._image = image
        self._uuid = uuid
        self._is_active = is_active
        self._validator = ProductValidator(self, repository)
        self.validator.validate()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    @property
    def validator(self):
        return self._validator
