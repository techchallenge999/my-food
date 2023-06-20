from typing import Optional
from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.use_cases.user.find.find_usuario_dto import (
    FindUserInputDto,
    FindUserOutputDto,
)


class FindUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, input: FindUserInputDto) -> Optional[FindUserOutputDto]:
        user = self._repository.find(uuid=input.uuid)

        if user is None:
            return None

        return FindUserOutputDto(
            cpf=user.cpf, email=user.email, name=user.name, uuid=user.uuid
        )
