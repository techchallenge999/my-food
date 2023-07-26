from dataclasses import dataclass

from src.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


@dataclass
class ActivateProductInputDto:
    uuid: str


@dataclass
class ActivateProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str


@dataclass
class DeactivateProductInputDto:
    uuid: str


@dataclass
class DeactivateProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str
