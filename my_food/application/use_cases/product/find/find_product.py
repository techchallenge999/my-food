from typing import Optional
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)


class FindProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: FindProductInputDto, creator_uuid: str
    ) -> Optional[FindProductOutputDto]:
        creator = self._user_repository.find(creator_uuid)

        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            return None

        if (creator is None or not creator.is_admin) and not product.is_active:
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
