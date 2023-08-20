from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.shared.exceptions.base import DomainException
from src.domain.shared.exceptions.user import Unauthorized
from src.infrastructure.fast_api.utils.auth import get_current_user
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.interface_adapters.controllers.user import UserController
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.use_cases.user.find.find_user_dto import FindUserOutputDto
from src.use_cases.user.list.list_user_dto import ListUserOutputDto
from src.use_cases.user.update.update_user_dto import (
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
    input_data: UpdateUserInputDto,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        return UserController(UserRepository()).update_me(input_data, current_user)
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
        return UserController(UserRepository()).list_users(current_user)
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


@router.get("/{user_uuid}/", response_model=Optional[FindUserOutputDto])
async def retrieve_user(
    user_uuid: str,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        return UserController(UserRepository()).retrieve_user(user_uuid, current_user)
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
    input_data: UpdateUserInputDto,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        return UserController(UserRepository()).update_user(input_data, current_user)
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
    input_data: CreateUserInputDto,
    current_user: Annotated[FindUserOutputDto, Depends(get_current_user)],
):
    try:
        return UserController(UserRepository()).create_admin_user(
            input_data, current_user
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
