from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from src.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
    ProductCategory,
)
from src.application.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class ProductRepositoryDto:
    name: str
    category: ProductCategory
    price: float
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
    def list(self) -> Optional[List[ProductRepositoryDto]]:
        pass

    @abstractmethod
    def update(self, entity: ProductInterface) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
