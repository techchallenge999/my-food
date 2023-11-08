from uuid import uuid4

from src.domain.aggregates.user.entities.user import User
from src.domain.aggregates.user.value_objects.cpf import Cpf
from src.domain.aggregates.user.value_objects.email import Email
from src.domain.aggregates.user.value_objects.password import Password
from src.domain.shared.exceptions.user import UnauthorizedException
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface
from src.interface_adapters.gateways.sign_up_microservice import (
    SignUpInputDto,
    SignUpMicroserviceInterface,
)
from src.use_cases.user.create.create_user_dto import (
    CreateUserInputDto,
    CreateUserOutputDto,
)


class CreateUserUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        sign_up_microservice: SignUpMicroserviceInterface,
    ):
        self._repository = repository
        self._sign_up_microservice = sign_up_microservice

    def execute(self, input_data: CreateUserInputDto) -> CreateUserOutputDto:
        cpf = "".join(filter(str.isdigit, input_data.cpf))

        new_user = User(
            cpf=Cpf(cpf),
            email=Email(input_data.email),
            name=input_data.name,
            password=Password(input_data.password),
            repository=self._repository,
            uuid=uuid4(),
        )

        new_user_dto = CreateUserOutputDto(
            cpf=new_user.cpf,
            email=new_user.email,
            name=new_user.name,
            is_admin=new_user.is_admin,
            uuid=new_user.uuid,
        )

        self._repository.create(new_user_dto=new_user_dto)

        self._sign_up_microservice.save(
            sign_up_input_dto=SignUpInputDto(
                cpf=new_user.cpf,
                is_admin=new_user.is_admin,
                password=new_user.password,
                uuid=new_user.uuid,
            )
        )

        return new_user_dto


class CreateAdminUserUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        sign_up_microservice: SignUpMicroserviceInterface,
    ):
        self._repository = repository
        self._sign_up_microservice = sign_up_microservice

    def execute(
        self, input_data: CreateUserInputDto, creator_uuid: str
    ) -> CreateUserOutputDto:
        user = self._repository.find(creator_uuid)

        if user is None or not user.is_admin:
            raise UnauthorizedException("User not Allowed!")

        cpf = "".join(filter(str.isdigit, input_data.cpf))

        new_user = User(
            cpf=Cpf(cpf),
            email=Email(input_data.email),
            name=input_data.name,
            password=Password(input_data.password),
            repository=self._repository,
            is_admin=True,
            uuid=uuid4(),
        )

        new_user_dto = CreateUserOutputDto(
            cpf=new_user.cpf,
            email=new_user.email,
            name=new_user.name,
            is_admin=new_user.is_admin,
            uuid=new_user.uuid,
        )

        self._repository.create(new_user_dto=new_user_dto)

        self._sign_up_microservice.save(
            sign_up_input_dto=SignUpInputDto(
                cpf=new_user.cpf,
                is_admin=new_user.is_admin,
                password=new_user.password,
                uuid=new_user.uuid,
            )
        )

        return new_user_dto
