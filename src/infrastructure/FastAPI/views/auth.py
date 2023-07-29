from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict

from src.application.use_cases.user.create.create_user import CreateUserUseCase
from src.application.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.infrastructure.FastAPI.utils.auth import (
    create_access_token,
    get_user_by_cpf,
    raise_credentials_exception,
    verify_password,
)
from src.infrastructure.FastAPI.utils.schemas import TokenModel
from src.infrastructure.postgresql.repositories.user.user import UserRepository


router = APIRouter()


@router.post("/sign-up", status_code=201)
async def sign_up(input_data: CreateUserInputDto) -> CreateUserOutputDto:
    repository = UserRepository()
    create_use_case = CreateUserUseCase(repository)
    new_user = create_use_case.execute(
        CreateUserInputDto(
            cpf=input_data.cpf,
            email=input_data.email,
            name=input_data.name,
            password=input_data.password,
        )
    )
    return new_user


@router.post("/token", response_model=TokenModel)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]):
    user = await get_user_by_cpf(form_data.username)
    if not (user and verify_password(form_data.password, user.password)):
        raise_credentials_exception("Incorrect username or password")
    access_token = create_access_token({"sub": user.cpf})
    return {"access_token": access_token, "token_type": "bearer"}