from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class ProductCategory(Enum):
    SNACK = "lanche"
    SIDE_DISH = "acompanhamento"
    DRINK = "bebida"
    DESSERT = "sobremesa"


class ProductInterface(ABC):
    _name: str
    _category: ProductCategory
    _price: str
    _description: str
    _image: bytes
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def category(self) -> ProductCategory:
        pass

    @category.setter
    @abstractmethod
    def category(self, value: ProductCategory):
        pass

    @property
    @abstractmethod
    def price(self) -> str:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: str):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def image(self) -> bytes:
        pass

    @image.setter
    @abstractmethod
    def image(self, value: bytes):
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass