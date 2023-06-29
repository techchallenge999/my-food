from my_food.application.domain.aggregates.product.entities.product import Product
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.use_cases.product.create.create_product_dto import (
    CreateProductInputDto,
    CreateProductOutputDto,
)


class CreateProductUseCase:
    def __init__(self, repository: ProductRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: CreateProductInputDto) -> CreateProductOutputDto:
        new_product = Product(
            name=input_data.name,
            category=input_data.category,
            price=input_data.price,
            description=input_data.description,
            image=input_data.image,
            repository=self._repository,
        )

        self._repository.create(entity=new_product)

        return CreateProductOutputDto(
            name=new_product.name,
            category=new_product.category,
            price=new_product.price,
            description=new_product.description,
            image=new_product.image,
            uuid=new_product.uuid,
        )
