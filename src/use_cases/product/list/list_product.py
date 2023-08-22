from typing import List, Optional
from src.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.domain.shared.exceptions.product import (
    InvalidProductCategoryException,
)
from src.use_cases.product.list.list_product_dto import (
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

    def execute(
        self, actor_uuid: str | None, filters: dict = {}
    ) -> Optional[List[ListProductOutputDto]]:
        actor = self._user_repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            filters["is_active"] = True
        if "category" in filters.keys():
            try:
                ProductCategory(filters["category"])
            except ValueError as err:
                raise InvalidProductCategoryException(err.args[0])

        product_list = self._repository.list(filters)

        if product_list is None:
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
            for product in product_list
        ]
