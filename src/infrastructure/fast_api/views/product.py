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
from src.infrastructure.postgresql.repositories.user import UserRepository
from src.domain.aggregates.product.interfaces.product_entity import (
    ProductCategory,
)
from src.domain.shared.exceptions.base import DomainException
from src.domain.shared.exceptions.user import Unauthorized
from src.interface_adapters.controllers.product import ProductController
from src.use_cases.product.activation.activation_product_dto import (
    ActivateProductInputDto,
    ActivateProductOutputDto,
    DeactivateProductInputDto,
    DeactivateProductOutputDto,
)
from src.use_cases.product.create.create_product_dto import (
    CreateProductOutputDto,
)
from src.use_cases.product.delete.delete_product_dto import (
    DeleteProductOutputDto,
)
from src.use_cases.product.find.find_product_dto import (
    FindProductOutputDto,
)
from src.infrastructure.fast_api.utils.auth import (
    EmptyUser,
    get_current_user,
    get_current_user_optional,
)
from src.infrastructure.postgresql.repositories.product import ProductRepository
from src.use_cases.product.list.list_product_dto import (
    ListProductOutputDto,
)
from src.use_cases.product.update.update_product_dto import (
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
        return ProductController(
            ProductRepository(), UserRepository(), current_user
        ).list_products(category)
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
        return ProductController(
            ProductRepository(), UserRepository(), current_user
        ).retrieve_product(product_uuid)
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
        image_contents = await image.read()
        return await ProductController(
            ProductRepository(), UserRepository(), current_user
        ).update_product(name, category, price, description, image_contents, uuid)
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
        image_contents = await image.read()
        return await ProductController(
            ProductRepository(), UserRepository(), current_user
        ).create_product(name, category, price, description, image_contents)
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
        return ProductController(
            ProductRepository(), UserRepository(), current_user
        ).activate_product(input_data)
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
        return ProductController(
            ProductRepository(), UserRepository(), current_user
        ).deactivate_product(input_data)
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
        return ProductController(
            ProductRepository(), UserRepository(), current_user
        ).delete_product(product_uuid)
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
