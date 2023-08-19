from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from src.interface_adapters.controllers.auth import AuthController
from src.interface_adapters.gateways.auth import FindUserParserGateway
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.infrastructure.FastAPI.utils.auth import (
    create_access_token,
    raise_credentials_exception,
    verify_password,
)
from src.infrastructure.FastAPI.utils.schemas import TokenModel
from src.infrastructure.postgresql.repositories.user.user import UserRepository


router = APIRouter()


@router.post("/sign-up", status_code=201)
async def sign_up(input_data: CreateUserInputDto) -> CreateUserOutputDto:
    return AuthController(UserRepository()).sign_up(input_data)


@router.post("/token", response_model=TokenModel)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]
) -> dict:
    find_user_parser_gateway = FindUserParserGateway(form_data.username)
    user = AuthController(UserRepository()).find_user_by_cpf(find_user_parser_gateway)

    if not (user is not None and verify_password(form_data.password, user.password)):
        raise_credentials_exception("Incorrect username or password")

    access_token = create_access_token({"sub": user.cpf})
    return {"access_token": access_token, "token_type": "bearer"}
