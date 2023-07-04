from typing import List, Optional

from my_food.adapters.postgresql.models.product.product import ProductModel
from my_food.application.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
    ProductInterface,
)
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
    ProductRepositoryInterface,
)


class ProductRepository(ProductRepositoryInterface):
    def create(self, entity: ProductInterface) -> None:
        new_product = ProductModel(
            name=entity.name,
            category=entity.category,
            price=entity.price,
            description=entity.description,
            image=entity.image,
            uuid=entity.uuid,
        )
        new_product.create()

    def find(self, uuid: str) -> Optional[ProductRepositoryDto]:
        product = ProductModel.retrieve(uuid)
        if product is None:
            return None
        return ProductRepositoryDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=str(product.uuid),
        )

    def update(self, entity: ProductInterface) -> None:
        product = ProductModel.retrieve(entity.uuid)
        if product:
            ProductModel.update(
                {
                    "name": entity.name,
                    "category": entity.category,
                    "price": entity.price,
                    "description": entity.description,
                    "image": entity.image,
                    "uuid": entity.uuid,
                    "is_active": entity.is_active,
                    "id": product.id,
                }
            )

    def list(self) -> Optional[ProductRepositoryDto]:
        products = ProductModel.list()

        return [
            ProductRepositoryDto(
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                is_active=product.is_active,
                uuid=str(product.uuid),
            )
            for product in products
        ]

    def delete(self, uuid: str) -> Optional[ProductRepositoryDto]:
        product = ProductModel.retrieve(uuid)
        if product is None:
            return None
        ProductModel.destroy(product.uuid)
        return ProductRepositoryDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=str(product.uuid),
        )

    def filter_by_category(
        self, category: ProductCategory
    ) -> Optional[List[ProductRepositoryDto]]:
        products = ProductModel.list_filtering_by_column("category", category)

        return [
            ProductRepositoryDto(
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                is_active=product.is_active,
                uuid=str(product.uuid),
            )
            for product in products
        ]

    def list_active(self) -> Optional[ProductRepositoryDto]:
        products = ProductModel.list_filtering_by_column("is_active", True)

        return [
            ProductRepositoryDto(
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                is_active=product.is_active,
                uuid=str(product.uuid),
            )
            for product in products
        ]
