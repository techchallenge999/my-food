from dataclasses import dataclass

from src.domain.aggregates.product.interfaces.product import (
    ProductCategory,
)


@dataclass
class UpdateProductInputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    uuid: str


@dataclass
class UpdateProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str
