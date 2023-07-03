from typing import List, Optional
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.product.list.list_product_dto import (
    ListProductOutputDto,
)


class ListProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(self, creator_uuid: str) -> Optional[List[ListProductOutputDto]]:
        creator = self._user_repository.find(creator_uuid)
        if creator is None or not creator.is_admin:
            products_list = self._repository.list_active()
        else:
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
