from src.domain.shared.exceptions.product import ProductNotFoundException
from src.infrastructure.postgresql.models.product import ProductModel
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryDto,
    ProductRepositoryInterface,
)
from src.use_cases.product.create.create_product_dto import CreateProductOutputDto
from src.use_cases.product.update.update_product_dto import UpdateProductOutputDto


class ProductRepository(ProductRepositoryInterface):
    def create(self, new_product_dto: CreateProductOutputDto) -> None:
        new_product = ProductModel(
            name=new_product_dto.name,
            category=new_product_dto.category,
            price=new_product_dto.price,
            description=new_product_dto.description,
            image=new_product_dto.image,
            is_active=new_product_dto.is_active,
            uuid=new_product_dto.uuid,
        )
        new_product.create()

    def find(self, uuid: str) -> ProductRepositoryDto:
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

    def list(self, filters: dict) -> list[ProductRepositoryDto]:
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

    def update(self, updated_product_dto: UpdateProductOutputDto) -> None:
        product = ProductModel.retrieve(updated_product_dto.uuid)
        if product:
            ProductModel.update(
                {
                    "name": updated_product_dto.name,
                    "category": updated_product_dto.category,
                    "price": updated_product_dto.price,
                    "description": updated_product_dto.description,
                    "image": updated_product_dto.image,
                    "uuid": updated_product_dto.uuid,
                    "is_active": updated_product_dto.is_active,
                    "id": product.id,
                }
            )

    def delete(self, uuid: str) -> ProductRepositoryDto | None:
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
