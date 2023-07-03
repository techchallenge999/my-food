from typing import Optional
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.user.list.list_user_dto import (
    ListUserOutputDto,
)


class ListUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, actor_uuid: str) -> Optional[ListUserOutputDto]:
        actor = self._repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            return None

        users = self._repository.list()

        if users is None:
            return None

        return [
            ListUserOutputDto(
                cpf=user.cpf,
                email=user.email,
                name=user.name,
                is_admin=user.is_admin,
                uuid=user.uuid,
            )
            for user in users
        ]