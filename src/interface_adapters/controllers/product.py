from src.domain.aggregates.product.interfaces.product import ProductCategory
from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.interface_adapters.gateways.repositories.product import (
    ProductRepositoryInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.interface_adapters.utils.image import bytes_to_base_64
from src.use_cases.product.activation.activation_product_dto import (
    ActivateProductInputDto,
    ActivateProductOutputDto,
    DeactivateProductInputDto,
    DeactivateProductOutputDto,
)
from src.use_cases.product.activation.activation_update_product import (
    ActivateProductUseCase,
    DeactivateProductUseCase,
)
from src.use_cases.product.create.create_product import CreateProductUseCase
from src.use_cases.product.create.create_product_dto import (
    CreateProductInputDto,
    CreateProductOutputDto,
)
from src.use_cases.product.delete.delete_product import DeleteProductUseCase
from src.use_cases.product.delete.delete_product_dto import (
    DeleteProductInputDto,
    DeleteProductOutputDto,
)
from src.use_cases.product.find.find_product import FindProductUseCase
from src.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)
from src.use_cases.product.list.list_product import ListProductUseCase
from src.use_cases.product.list.list_product_dto import ListProductOutputDto
from src.use_cases.product.update.update_product import UpdateProductUseCase
from src.use_cases.product.update.update_product_dto import (
    UpdateProductInputDto,
    UpdateProductOutputDto,
)


class ProductController:
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        user_repository: UserRepositoryInterface,
        current_user: AuthorizationOutputDto,
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.current_user = current_user

    def list_products(self, category: str | None = None) -> list[ListProductOutputDto]:
        filters = {}
        if category is not None:
            filters["category"] = ProductCategory(category).name

        list_use_case = ListProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )

        return list_use_case.execute(self.current_user.uuid, filters)

    def retrieve_product(self, product_uuid: str) -> FindProductOutputDto | None:
        find_use_case = FindProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return find_use_case.execute(
            FindProductInputDto(uuid=product_uuid), self.current_user.uuid
        )

    async def update_product(
        self,
        name: str,
        category: ProductCategory,
        price: float,
        description: str,
        image_contents: bytes,
        uuid: str,
    ) -> UpdateProductOutputDto:
        input_data = UpdateProductInputDto(
            name=name,
            category=category,
            price=price,
            description=description,
            image=bytes_to_base_64(image_contents),
            uuid=uuid,
        )
        update_use_case = UpdateProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=self.current_user.uuid
        )

    async def create_product(
        self,
        name: str,
        category: ProductCategory,
        price: float,
        description: str,
        image_contents: bytes,
    ) -> CreateProductOutputDto:
        input_data = CreateProductInputDto(
            name=name,
            category=category,
            price=price,
            description=description,
            image=bytes_to_base_64(image_contents),
        )
        create_use_case = CreateProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return create_use_case.execute(input_data, self.current_user.uuid)

    def activate_product(
        self,
        input_data: ActivateProductInputDto,
    ) -> ActivateProductOutputDto:
        update_use_case = ActivateProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=self.current_user.uuid
        )

    def deactivate_product(
        self,
        input_data: DeactivateProductInputDto,
    ) -> DeactivateProductOutputDto:
        update_use_case = DeactivateProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=self.current_user.uuid
        )

    def delete_product(
        self,
        product_uuid: str,
    ) -> DeleteProductOutputDto | None:
        delete_use_case = DeleteProductUseCase(
            repository=self.repository, user_repository=self.user_repository
        )
        return delete_use_case.execute(
            DeleteProductInputDto(uuid=product_uuid), self.current_user.uuid
        )
