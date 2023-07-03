from my_food.application.domain.aggregates.user.entities.user import User
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)


class CreateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: CreateUserInputDto) -> CreateUserOutputDto:
        cpf = "".join(filter(str.isdigit, input_data.cpf))

        new_user = User(
            cpf=cpf,
            email=input_data.email,
            name=input_data.name,
            password=input_data.password,
            repository=self._repository,
        )

        self._repository.create(entity=new_user)

        return CreateUserOutputDto(
            cpf=new_user.cpf,
            email=new_user.email,
            name=new_user.name,
            is_admin=new_user.is_admin,
            uuid=new_user.uuid,
        )


class CreateAdminUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(
        self, input_data: CreateUserInputDto, creator_uuid: str
    ) -> CreateUserOutputDto:
        user = self._repository.find(creator_uuid.uuid)

        if user is None or not user.is_admin:
            return None

        cpf = "".join(filter(str.isdigit, input_data.cpf))

        new_user = User(
            cpf=cpf,
            email=input_data.email,
            name=input_data.name,
            password=input_data.password,
            repository=self._repository,
            is_admin=True,
        )

        self._repository.create(entity=new_user)

        return CreateUserOutputDto(
            cpf=new_user.cpf,
            email=new_user.email,
            name=new_user.name,
            is_admin=new_user.is_admin,
            uuid=new_user.uuid,
        )