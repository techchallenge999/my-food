from typing import Optional
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.use_cases.product.find.find_product_dto import (
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
        self, input_data: FindProductInputDto, actor_uuid: str | None
    ) -> Optional[FindProductOutputDto]:
        actor = self._user_repository.find(actor_uuid)

        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            return None

        if (actor is None or not actor.is_admin) and not product.is_active:
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
