from dataclasses import dataclass

from src.domain.aggregates.product.interfaces.product import (
    ProductCategory,
)


@dataclass
class FindProductInputDto:
    uuid: str


@dataclass
class FindProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str
