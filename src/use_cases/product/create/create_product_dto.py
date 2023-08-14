from dataclasses import dataclass

from src.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


@dataclass
class CreateProductInputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes


@dataclass
class CreateProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str
