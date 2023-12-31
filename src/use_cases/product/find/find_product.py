from src.domain.shared.exceptions.product import (
    ProductNotFoundException,
    UnavailableProductException,
)
from src.domain.shared.exceptions.user import UnauthorizedException
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
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
    ) -> FindProductOutputDto | None:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise UnauthorizedException()

        product = self._repository.find(uuid=input_data.uuid)

        if product is None:
            raise ProductNotFoundException()
        if not product.is_active:
            raise UnavailableProductException()

        return FindProductOutputDto(
            name=product.name,
            category=product.category,
            price=product.price,
            description=product.description,
            image=product.image,
            is_active=product.is_active,
            uuid=product.uuid,
        )
