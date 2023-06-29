from dataclasses import dataclass

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


@dataclass
class UpdateProductInputDto:
    name: str
    category: ProductCategory
    price: str
    description: str
    image: bytes
    uuid: str


@dataclass
class UpdateProductOutputDto:
    name: str
    category: ProductCategory
    price: str
    description: str
    image: bytes
    uuid: str
