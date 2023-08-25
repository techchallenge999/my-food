from src.domain.shared.exceptions.user import UnauthorizedException
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.user.list.list_user_dto import ListUserOutputDto


class ListUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, actor_uuid: str) -> list[ListUserOutputDto]:
        actor = self._repository.find(actor_uuid)
        if actor is None or not actor.is_admin:
            raise UnauthorizedException("User not Allowed!")

        users = self._repository.list()

        if users is None:
            return []

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
