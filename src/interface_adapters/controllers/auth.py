from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.interface_adapters.gateways.sign_up_microservice import (
    SignUpMicroserviceInterface,
)
from src.use_cases.user.create.create_user import CreateUserUseCase
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)
from src.use_cases.user.find.find_user_dto import (
    FindUserByCpfOutputDto,
)


class AuthController:
    def sign_up(
        self,
        input_data: CreateUserInputDto,
        sign_up_microservice: SignUpMicroserviceInterface,
        user_repository: UserRepositoryInterface,
    ) -> CreateUserOutputDto:
        new_user = CreateUserUseCase(
            repository=user_repository, sign_up_microservice=sign_up_microservice
        ).execute(input_data)
        return new_user

    def find_user_by_cpf(self, cpf: str) -> FindUserByCpfOutputDto:
        pass
        # user = FindUserByCpfUseCase(self.repository).execute(
        #     FindUserByCpfInputDto(cpf=cpf), actor_cpf=cpf
        # )
        # return user
