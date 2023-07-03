from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
    ProductCategory,
)
from my_food.application.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class ProductRepositoryDto:
    name: str
    category: ProductCategory
    price: str
    description: str
    image: bytes
    is_active: bool
    uuid: str


class ProductRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: ProductInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[ProductRepositoryDto]:
        pass

    @abstractmethod
    def list(self, uuid: str) -> Optional[List[ProductRepositoryDto]]:
        pass

    @abstractmethod
    def update(self, entity: ProductInterface) -> None:
        pass

    @abstractmethod
    def filter_by_category(self, category: str) -> Optional[List[ProductRepositoryDto]]:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
