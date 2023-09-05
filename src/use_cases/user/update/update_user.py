from uuid import UUID

from src.domain.aggregates.user.entities.user import User
from src.domain.aggregates.user.value_objects.cpf import Cpf
from src.domain.aggregates.user.value_objects.email import Email
from src.domain.aggregates.user.value_objects.password import Password
from src.domain.shared.exceptions.user import (
    UnauthorizedException,
    UserNotFoundException,
)
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.user.update.update_user_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)


class UpdateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(
        self, input_data: UpdateUserInputDto, actor_uuid: str
    ) -> UpdateUserOutputDto:
        actor = self._repository.find(actor_uuid)
        if actor is None or (input_data.uuid != actor_uuid and not actor.is_admin):
            raise UnauthorizedException("User not Allowed!")

        user = self._repository.find(input_data.uuid)

        if user is None:
            raise UserNotFoundException()

        cpf = "".join(filter(str.isdigit, user.cpf))
        updated_user = User(
            cpf=Cpf(cpf),
            email=Email(input_data.email),
            name=input_data.name,
            password=Password(user.password),
            repository=self._repository,
            is_admin=user.is_admin,
            uuid=UUID(input_data.uuid),
        )

        updated_user_dto = UpdateUserOutputDto(
            cpf=updated_user.cpf,
            email=updated_user.email,
            name=updated_user.name,
            is_admin=updated_user.is_admin,
            uuid=updated_user.uuid,
        )

        self._repository.update(updated_user_dto, updated_user.password)

        return updated_user_dto
