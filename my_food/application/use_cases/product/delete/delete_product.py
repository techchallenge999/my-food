from typing import Optional
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.product.delete.delete_product_dto import (
    DeleteProductInputDto,
    DeleteProductOutputDto,
)


class DeleteProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: DeleteProductInputDto, actor_uuid: str
    ) -> Optional[DeleteProductOutputDto]:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            return None

        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            return None

        self._repository.delete(uuid=input_data.uuid)

        return DeleteProductOutputDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=product.uuid,
        )
