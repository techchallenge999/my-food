from typing import Optional
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)


class FindProductUseCase:
    def __init__(self, repository: ProductRepositoryInterface):
        self._repository = repository

    def execute(
        self, input_data: FindProductInputDto
    ) -> Optional[FindProductOutputDto]:
        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            return None

        return FindProductOutputDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=product.uuid,
        )
