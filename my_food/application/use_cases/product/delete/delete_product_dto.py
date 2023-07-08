from dataclasses import dataclass

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


@dataclass
class DeleteProductInputDto:
    uuid: str


@dataclass
class DeleteProductOutputDto:
    name: str
    category: ProductCategory
    price: float
    description: str
    image: bytes
    is_active: bool
    uuid: str
