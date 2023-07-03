from uuid import UUID
from my_food.application.domain.aggregates.product.entities.product import Product
from my_food.application.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
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
        self, input_data: UpdateProductInputDto, creator_uuid: str
    ) -> UpdateProductOutputDto:
        creator = self._user_repository.find(creator_uuid)
        if creator is None or not creator.is_admin:
            return None

        product = self._repository.find(input_data.uuid)

        if product is None:
            return None

        updated_product = Product(
            name=input_data.name,
            category=input_data.category,
            price=input_data.price,
            description=input_data.description,
            image=input_data.image,
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
            uuid=updated_product.uuid,
        )
