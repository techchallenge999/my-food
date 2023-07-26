from typing import List, Optional
from src.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.application.domain.shared.errors.exceptions.user import Unauthorized
from src.application.use_cases.user.list.list_user_dto import (
    ListUserOutputDto,
)


class ListUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, actor_uuid: str) -> Optional[List[ListUserOutputDto]]:
        actor = self._repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise Unauthorized("User not Allowed!")

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
