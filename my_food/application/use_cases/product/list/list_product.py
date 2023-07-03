from typing import List, Optional
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.use_cases.product.list.list_product_dto import (
    ListProductOutputDto,
)


class ListProductUseCase:
    def __init__(self, repository: ProductRepositoryInterface):
        self._repository = repository

    def execute(self) -> Optional[List[ListProductOutputDto]]:
        products_list = self._repository.list()

        if products_list is None:
            return None

        return [
            ListProductOutputDto(
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                is_active=product.is_active,
                uuid=product.uuid,
            )
            for product in products_list
        ]
