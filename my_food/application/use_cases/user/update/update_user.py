from typing import Optional
from uuid import UUID
from my_food.application.domain.aggregates.user.entities.user import User
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.user.update.update_user_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)


class UpdateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: UpdateUserInputDto) -> Optional[UpdateUserOutputDto]:
        user = self._repository.find(input_data.uuid)

        if user is None:
            return None

        updated_user = User(
            cpf=input_data.cpf,
            email=input_data.email,
            name=input_data.name,
            password=user.password,
            repository=self._repository,
            uuid=UUID(input_data.uuid),
        )

        self._repository.update(updated_user)

        return UpdateUserOutputDto(
            cpf=updated_user.cpf,
            email=updated_user.email,
            name=updated_user.name,
            uuid=updated_user.uuid,
        )
