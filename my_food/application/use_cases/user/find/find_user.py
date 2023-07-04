from typing import Optional
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.user import Unauthorized
from my_food.application.use_cases.user.find.find_user_dto import (
    FindUserByCpfInputDto,
    FindUserByCpfOutputDto,
    FindUserInputDto,
    FindUserOutputDto,
)


class FindUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(
        self, input_data: FindUserInputDto, actor_uuid: str
    ) -> Optional[FindUserOutputDto]:
        actor = self._repository.find(actor_uuid)
        if actor is None or (input_data.uuid != actor_uuid and not actor.is_admin):
            raise Unauthorized("User not Allowed!")

        user = self._repository.find(uuid=input_data.uuid)

        if user is None:
            return None

        return FindUserOutputDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            is_admin=user.is_admin,
            uuid=user.uuid,
        )


class FindUserByCpfUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(
        self, input_data: FindUserByCpfInputDto, actor_cpf: str
    ) -> Optional[FindUserByCpfOutputDto]:
        actor = self._repository.find_by_cpf(cpf=actor_cpf)
        if actor is None or (input_data.cpf != actor.cpf and not actor.is_admin):
            raise Unauthorized("User not Allowed!")

        cpf = "".join(filter(str.isdigit, input_data.cpf))

        user = self._repository.find_by_cpf(cpf=cpf)

        if user is None:
            return None

        return FindUserByCpfOutputDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            is_admin=user.is_admin,
            uuid=user.uuid,
        )
