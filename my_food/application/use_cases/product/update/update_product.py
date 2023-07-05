from uuid import UUID
from my_food.application.domain.aggregates.product.entities.product import Product
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.product import (
    UnavailableProductException,
)
from my_food.application.domain.shared.errors.exceptions.user import Unauthorized
from my_food.application.use_cases.product.update.update_product_dto import (
    UpdateProductInputDto,
    UpdateProductOutputDto,
)


class UpdateProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: UpdateProductInputDto, actor_uuid: str
    ) -> UpdateProductOutputDto:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise Unauthorized("User not Allowed!")

        product = self._repository.find(input_data.uuid)

        if product is None:
            raise UnavailableProductException("Product Not Found!")

        updated_product = Product(
            name=input_data.name,
            category=input_data.category,
            price=input_data.price,
            description=input_data.description,
            image=input_data.image,
            is_active=product.is_active,
            uuid=UUID(input_data.uuid),
            repository=self._repository,
        )

        self._repository.update(entity=updated_product)

        return UpdateProductOutputDto(
            name=updated_product.name,
            category=updated_product.category,
            price=updated_product.price,
            description=updated_product.description,
            image=updated_product.image,
            is_active=product.is_active,
            uuid=updated_product.uuid,
        )
