from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.use_cases.user.create.create_user import CreateAdminUserUseCase
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.use_cases.user.find.find_user import FindUserByCpfUseCase, FindUserUseCase
from src.use_cases.user.find.find_user_dto import (
    FindUserByCpfInputDto,
    FindUserByCpfOutputDto,
    FindUserInputDto,
    FindUserOutputDto,
)
from src.use_cases.user.list.list_user import ListUserUseCase
from src.use_cases.user.list.list_user_dto import ListUserOutputDto
from src.use_cases.user.update.update_user import UpdateUserUseCase
from src.use_cases.user.update.update_user_dto import (
    UpdateUserInputDto,
    UpdateUserOutputDto,
)


class UserController:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def update_me(
        self, input_data: UpdateUserInputDto, current_user: FindUserOutputDto
    ) -> UpdateUserOutputDto:
        update_use_case = UpdateUserUseCase(self.repository)
        updated_user = update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
        return updated_user

    def list_users(self, current_user: FindUserOutputDto) -> list[ListUserOutputDto]:
        list_use_case = ListUserUseCase(self.repository)
        return list_use_case.execute(current_user.uuid)

    def retrieve_user(
        self, user_uuid: str, current_user: FindUserOutputDto
    ) -> FindUserOutputDto | None:
        find_use_case = FindUserUseCase(self.repository)
        user = find_use_case.execute(
            FindUserInputDto(uuid=user_uuid), current_user.uuid
        )
        return user

    def update_user(
        self, input_data: UpdateUserInputDto, current_user: FindUserOutputDto
    ) -> UpdateUserOutputDto:
        update_use_case = UpdateUserUseCase(self.repository)
        updated_user = update_use_case.execute(
            input_data=input_data, actor_uuid=current_user.uuid
        )
        return updated_user

    def create_admin_user(
        self, input_data: CreateUserInputDto, current_user: FindUserOutputDto
    ) -> CreateUserOutputDto:
        create_use_case = CreateAdminUserUseCase(self.repository)
        new_admin_user = create_use_case.execute(input_data, current_user.uuid)
        return new_admin_user

    def find_user_by_cpf(
        self, cpf: str, actor_cpf: str
    ) -> FindUserByCpfOutputDto | None:
        find_use_case = FindUserByCpfUseCase(self.repository)
        user = find_use_case.execute(
            FindUserByCpfInputDto(cpf=cpf), actor_cpf=actor_cpf
        )
        return user
