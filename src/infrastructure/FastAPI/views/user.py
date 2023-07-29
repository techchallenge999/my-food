from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.domain.shared.errors.exceptions.base import DomainException
from src.application.domain.shared.errors.exceptions.user import Unauthorized
from src.application.use_cases.user.create.create_user import CreateAdminUserUseCase
from src.application.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.application.use_cases.user.find.find_user import FindUserUseCase

from src.application.use_cases.user.find.find_user_dto import (
    FindUserInputDto,
    FindUserOutputDto,
)
from src.infrastructure.FastAPI.utils.auth import get_current_user
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.application.use_cases.user.list.list_user import ListUserUseCase
from src.application.use_cases.user.list.list_user_dto import ListUserOutputDto


from src.application.use_cases.user.update.update_user import UpdateUserUseCase
from src.application.use_cases.user.update.update_user_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)


router = APIRouter()


@router.get("/me/", response_model=FindUserOutputDto)
async def read_users_me(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)]
):
    return current_user


@router.put("/me/", response_model=UpdateUserOutputDto)
async def update_users_me(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    input_data: UpdateUserInputDto,
):
    try:
        repository = UserRepository()
        update_use_case = UpdateUserUseCase(repository)
        return update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/", response_model=list[ListUserOutputDto])
async def list_users(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)]
):
    try:
        repository = UserRepository()
        list_use_case = ListUserUseCase(repository)
        return list_use_case.execute(current_user.uuid)
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


@router.get("/{user_uuid}/", response_model=FindUserOutputDto)
async def retrieve_user(
    user_uuid: str,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        repository = UserRepository()
        find_use_case = FindUserUseCase(repository)
        return find_use_case.execute(
            FindUserInputDto(uuid=user_uuid), current_user.uuid
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


@router.put("/", response_model=UpdateUserOutputDto)
async def update_user(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    input_data: UpdateUserInputDto,
):
    try:
        repository = UserRepository()
        update_use_case = UpdateUserUseCase(repository)
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


@router.post("/admin/", response_model=CreateUserOutputDto)
async def create_admin_user(
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
    input_data: CreateUserInputDto,
):
    try:
        repository = UserRepository()
        find_use_case = CreateAdminUserUseCase(repository)
        return find_use_case.execute(input_data, current_user.uuid)
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
