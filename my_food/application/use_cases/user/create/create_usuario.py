from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.domain.aggregates.user.entities.user import User
from my_food.application.use_cases.user.create.create_usuario_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, input: CreateUserInputDto) -> CreateUserOutputDto:
        new_user = User(
            cpf=input.cpf,
            email=input.email,
            name=input.name,
            password=input.password,
            repository=self._repository,
        )

        self._repository.create(entity=new_user)

        return CreateUserOutputDto(
            cpf=new_user.cpf,
            email=new_user.email,
            name=new_user.name,
            uuid=new_user.uuid,
        )
