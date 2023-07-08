from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID
from my_food.application.domain.shared.interfaces.validator import ValidatorInterface


class ProductCategory(Enum):
    lanche = "lanche"
    acompanhamento = "acompanhamento"
    bebida = "bebida"
    sobremesa = "sobremesa"


class ProductInterface(ABC):
    _name: str
    _category: ProductCategory
    _price: float
    _description: str
    _image: bytes
    _is_active: bool
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
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float):
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
    def is_active(self) -> bool:
        pass

    @is_active.setter
    @abstractmethod
    def is_active(self, value: bool):
        pass

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
