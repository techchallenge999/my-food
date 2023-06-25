from typing import Optional
from my_food.application.domain.aggregates.user.interfaces.user_repository import UserRepositoryInterface
from my_food.application.use_cases.user.find.find_user_dto import (
    FindUserByCpfInputDto,
    FindUserByCpfOutputDto,
    FindUserInputDto,
    FindUserOutputDto,
)


class FindUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindUserInputDto) -> Optional[FindUserOutputDto]:
        user = self._repository.find(uuid=input_data.uuid)

        if user is None:
            return None

        return FindUserOutputDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            uuid=user.uuid,
        )


class FindUserByCpfUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindUserByCpfInputDto) -> Optional[FindUserByCpfOutputDto]:
        cpf =  "".join(filter(str.isdigit, input_data.cpf))

        user = self._repository.find_by_cpf(cpf=cpf)

        if user is None:
            return None

        return FindUserByCpfOutputDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            uuid=user.uuid,
        )
