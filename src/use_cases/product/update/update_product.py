from uuid import UUID
from src.domain.aggregates.product.entities.product import Product
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.domain.shared.exceptions.product import (
    UnavailableProductException,
)
from src.domain.shared.exceptions.user import UnauthorizedException
from src.use_cases.product.update.update_product_dto import (
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
        self, input_data: UpdateProductInputDto, actor_uuid: str | None
    ) -> UpdateProductOutputDto:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise UnauthorizedException("User not Allowed!")

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

        updated_product_dto = UpdateProductOutputDto(
            name=updated_product.name,
            category=updated_product.category,
            price=updated_product.price,
            description=updated_product.description,
            image=updated_product.image,
            is_active=product.is_active,
            uuid=updated_product.uuid,
        )

        self._repository.update(updated_product_dto)

        return updated_product_dto
