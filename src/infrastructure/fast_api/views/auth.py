from fastapi import APIRouter

from src.infrastructure.boto.sign_up.sign_up_microservice import SignUpMicroservice
from src.infrastructure.postgresql.repositories.user import UserRepository
from src.interface_adapters.controllers.auth import AuthController
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)


router = APIRouter()


@router.post("/sign-up", status_code=201, response_model=CreateUserOutputDto)
async def sign_up(input_data: CreateUserInputDto):
    return AuthController().sign_up(
        input_data=input_data,
        sign_up_microservice=SignUpMicroservice(),
        user_repository=UserRepository(),
    )
