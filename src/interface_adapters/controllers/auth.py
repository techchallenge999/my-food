from typing import Optional
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.interface_adapters.gateways.auth import FindUserParser
from src.use_cases.user.create.create_user import CreateUserUseCase
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.use_cases.user.find.find_user import FindUserByCpfUseCase
from src.use_cases.user.find.find_user_dto import FindUserByCpfOutputDto


class AuthController:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def sign_up(self, input_data: CreateUserInputDto) -> CreateUserOutputDto:
        new_user = CreateUserUseCase(self.repository).execute(input_data)
        return new_user

    def find_user_by_cpf(
        self, auth_parser: FindUserParser
    ) -> Optional[FindUserByCpfOutputDto]:
        user = FindUserByCpfUseCase(self.repository).execute(
            auth_parser.get_dto(), actor_cpf=auth_parser.get_actor_cpf()
        )
        return user
