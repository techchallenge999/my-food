from abc import abstractmethod
from dataclasses import dataclass

from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.domain.shared.interfaces.repository import RepositoryInterface
from src.use_cases.product.create.create_product_dto import CreateProductOutputDto
from src.use_cases.product.update.update_product_dto import UpdateProductOutputDto


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
    def create(self, new_product_dto: CreateProductOutputDto) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> ProductRepositoryDto | None:
        pass

    @abstractmethod
    def list(self, filters: dict) -> list[ProductRepositoryDto]:
        pass

    @abstractmethod
    def update(self, updated_product_dto: UpdateProductOutputDto) -> None:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> None:
        pass
