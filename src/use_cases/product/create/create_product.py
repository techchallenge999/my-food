from uuid import uuid4
from src.domain.aggregates.product.entities.product import Product
from src.domain.shared.exceptions.user import UnauthorizedException
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.use_cases.product.create.create_product_dto import (
    CreateProductInputDto,
    CreateProductOutputDto,
)


class CreateProductUseCase:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def execute(
        self, input_data: CreateProductInputDto, actor_uuid: str | None
    ) -> CreateProductOutputDto:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise UnauthorizedException("User not Allowed!")

        new_product = Product(
            name=input_data.name,
            category=input_data.category,
            price=input_data.price,
            description=input_data.description,
            image=input_data.image,
            repository=self._repository,
            uuid=uuid4(),
        )

        new_product_dto = CreateProductOutputDto(
            name=new_product.name,
            category=new_product.category,
            price=new_product.price,
            description=new_product.description,
            image=new_product.image,
            is_active=new_product.is_active,
            uuid=new_product.uuid,
        )

        self._repository.create(new_product_dto)

        return new_product_dto
