from uuid import UUID
from src.domain.aggregates.product.entities.product import Product
from src.domain.aggregates.product.interfaces.product_repository import (
    ProductRepositoryInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.domain.shared.errors.exceptions.product import (
    UnavailableProductException,
)
from src.domain.shared.errors.exceptions.user import Unauthorized
from src.use_cases.product.activation.activation_product_dto import (
    ActivateProductInputDto,
    ActivateProductOutputDto,
    DeactivateProductInputDto,
    DeactivateProductOutputDto,
)


class ActivateProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: ActivateProductInputDto, actor_uuid: str
    ) -> ActivateProductOutputDto:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise Unauthorized("User not Allowed!")

        product = self._repository.find(input_data.uuid)

        if product is None:
            return UnavailableProductException("Product Not Found!")

        activated_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=UUID(input_data.uuid),
            repository=self._repository,
        )

        activated_product.activate()

        self._repository.update(entity=activated_product)

        return ActivateProductOutputDto(
            name=activated_product.name,
            category=activated_product.category,
            price=activated_product.price,
            description=activated_product.description,
            image=activated_product.image,
            is_active=activated_product.is_active,
            uuid=activated_product.uuid,
        )


class DeactivateProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: DeactivateProductInputDto, actor_uuid: str
    ) -> DeactivateProductOutputDto:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise Unauthorized("User not Allowed!")

        product = self._repository.find(input_data.uuid)

        if product is None:
            return UnavailableProductException("Product Not Found!")

        deactivated_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=UUID(product.uuid),
            repository=self._repository,
        )

        deactivated_product.deactivate()

        self._repository.deactivate(entity=deactivated_product)

        return DeactivateProductOutputDto(
            name=deactivated_product.name,
            category=deactivated_product.category,
            price=deactivated_product.price,
            description=deactivated_product.description,
            image=deactivated_product.image,
            is_active=deactivated_product.is_active,
            uuid=deactivated_product.uuid,
        )
