from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    Form,
    UploadFile,
)
from src.infrastructure.FastAPI.utils.image import bytes_to_base_64
from src.infrastructure.FastAPI.utils.schemas import EmptyUser
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)
from src.domain.shared.errors.exceptions.base import DomainException
from src.domain.shared.errors.exceptions.user import Unauthorized
from src.use_cases.product.activation.activation_update_product import (
    ActivateProductUseCase,
    DeactivateProductUseCase,
)
from src.use_cases.product.activation.activation_product_dto import (
    ActivateProductInputDto,
    ActivateProductOutputDto,
    DeactivateProductInputDto,
    DeactivateProductOutputDto,
)
from src.use_cases.product.create.create_product import (
    CreateProductUseCase,
)
from src.use_cases.product.create.create_product_dto import (
    CreateProductOutputDto,
    CreateProductInputDto,
)
from src.use_cases.product.delete.delete_product import (
    DeleteProductUseCase,
)
from src.use_cases.product.delete.delete_product_dto import (
    DeleteProductInputDto,
    DeleteProductOutputDto,
)
from src.use_cases.product.find.find_product import FindProductUseCase

from src.use_cases.product.find.find_product_dto import (
    FindProductInputDto,
    FindProductOutputDto,
)
from src.infrastructure.FastAPI.utils.auth import (
    get_current_user,
    get_current_user_optional,
)
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.use_cases.product.list.list_product import ListProductUseCase
from src.use_cases.product.list.list_product_dto import (
    ListProductOutputDto,
)


from src.use_cases.product.update.update_product import (
    UpdateProductUseCase,
)
from src.use_cases.product.update.update_product_dto import (
    UpdateProductInputDto,
    UpdateProductOutputDto,
)
from src.use_cases.user.find.find_user_dto import FindUserOutputDto


router = APIRouter()


@router.get("/", response_model=list[ListProductOutputDto])
async def list_products(
    current_user: Annotated[
        FindUserOutputDto | EmptyUser, Depends(get_current_user_optional)
    ],
    category: str | None = None,
):
    try:
        repository = ProductRepository()
        user_repository = UserRepository()
        filters = {}
        if category is not None:
            filters["category"] = ProductCategory(category).name
        list_use_case = ListProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return list_use_case.execute(current_user.uuid, filters)
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{product_uuid}/", response_model=FindProductOutputDto)
async def retrieve_product(
    product_uuid: str,
    current_user: Annotated[
        FindUserOutputDto | EmptyUser, Depends(get_current_user_optional)
    ],
):
    try:
        repository = ProductRepository()
        user_repository = UserRepository()
        find_use_case = FindProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return find_use_case.execute(
            FindProductInputDto(uuid=product_uuid), current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/", response_model=UpdateProductOutputDto)
async def update_product(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    name: Annotated[str, Form()],
    category: Annotated[ProductCategory, Form()],
    price: Annotated[float, Form()],
    description: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    uuid: Annotated[str, Form()],
):
    try:
        contents = await image.read()
        input_data = UpdateProductInputDto(
            name=name,
            category=category,
            price=price,
            description=description,
            image=bytes_to_base_64(contents),
            uuid=uuid,
        )
        repository = ProductRepository()
        user_repository = UserRepository()
        update_use_case = UpdateProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/", response_model=CreateProductOutputDto)
async def create_product(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    name: Annotated[str, Form()],
    category: Annotated[ProductCategory, Form()],
    price: Annotated[float, Form()],
    description: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
):
    try:
        contents = await image.read()
        input_data = CreateProductInputDto(
            name=name,
            category=category,
            price=price,
            description=description,
            image=bytes_to_base_64(contents),
        )
        repository = ProductRepository()
        user_repository = UserRepository()
        create_use_case = CreateProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return create_use_case.execute(input_data, current_user.uuid)
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/activate/", response_model=ActivateProductOutputDto)
async def activate_product(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    input_data: ActivateProductInputDto,
):
    try:
        repository = ProductRepository()
        user_repository = UserRepository()
        update_use_case = ActivateProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/deactivate/", response_model=DeactivateProductOutputDto)
async def deactivate_product(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    input_data: DeactivateProductInputDto,
):
    try:
        repository = ProductRepository()
        user_repository = UserRepository()
        update_use_case = DeactivateProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{product_uuid}/", response_model=DeleteProductOutputDto)
async def delete_product(
    product_uuid: str,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        repository = ProductRepository()
        user_repository = UserRepository()
        delete_use_case = DeleteProductUseCase(
            repository=repository, user_repository=user_repository
        )
        return delete_use_case.execute(
            DeleteProductInputDto(uuid=product_uuid), current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
