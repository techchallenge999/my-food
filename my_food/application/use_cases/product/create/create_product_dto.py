from dataclasses import dataclass

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)


@dataclass
class CreateProductInputDto:
    name: str
    category: ProductCategory
    price: str
    description: str
    image: bytes


@dataclass
class CreateProductOutputDto:
    name: str
    category: ProductCategory
    price: str
    description: str
    image: bytes
    uuid: str
