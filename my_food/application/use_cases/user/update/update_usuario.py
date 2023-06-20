from typing import Optional
from my_food.application.domain.aggregates.user.entities.user import User
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.user.update.update_usuario_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)


class UpdateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, input: UpdateUserInputDto) -> Optional[UpdateUserOutputDto]:
        user = self._repository.find(input.uuid)

        if user is None:
            return None
        updated_user = User(
            cpf=user.cpf,
        )
        self._repository.update(updated_user)

        return UpdateUserOutputDto(
            cpf=user.cpf, email=user.email, name=user.name, uuid=user.uuid
        )
