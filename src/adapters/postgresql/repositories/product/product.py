from typing import Optional

from src.adapters.postgresql.models.product.product import ProductModel
from src.application.domain.aggregates.product.interfaces.product_entity import (
    ProductInterface,
)
from src.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryDto,
    ProductRepositoryInterface,
)
from src.application.domain.shared.errors.exceptions.product import (
    ProductNotFoundException,
)


class ProductRepository(ProductRepositoryInterface):
    def create(self, entity: ProductInterface) -> None:
        new_product = ProductModel(
            name=entity.name,
            category=entity.category,
            price=entity.price,
            description=entity.description,
            image=entity.image,
            is_active=entity.is_active,
            uuid=entity.uuid,
        )
        new_product.create()

    def find(self, uuid: str) -> Optional[ProductRepositoryDto]:
        product = ProductModel.retrieve(uuid)
        if product is None:
            raise ProductNotFoundException()
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

    def list(self, filters) -> Optional[ProductRepositoryDto]:
        products = ProductModel.list_filtering_by_column(filters)

        if products is None:
            return []

        return [
            ProductRepositoryDto(
                name=product[0].name,
                category=product[0].category,
                price=product[0].price,
                description=product[0].description,
                image=product[0].image,
                is_active=product[0].is_active,
                uuid=str(product[0].uuid),
            )
            for product in products
        ]

    def delete(self, uuid: str) -> Optional[ProductRepositoryDto]:
        product = ProductModel.retrieve(uuid)
        if product is None:
            raise ProductNotFoundException()
        ProductModel.destroy(str(product.uuid))
        return ProductRepositoryDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=str(product.uuid),
        )
