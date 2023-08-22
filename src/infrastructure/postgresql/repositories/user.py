from src.domain.shared.exceptions.user import UserNotFoundException
from src.infrastructure.postgresql.models.user import UserModel
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryDto,
    UserRepositoryInterface,
)
from src.use_cases.user.create.create_user_dto import CreateUserOutputDto
from src.use_cases.user.update.update_user_dto import UpdateUserOutputDto


class UserRepository(UserRepositoryInterface):
    def create(self, new_user_dto: CreateUserOutputDto, password: str) -> None:
        new_user = UserModel(
            cpf=new_user_dto.cpf,
            email=new_user_dto.email,
            name=new_user_dto.name,
            password=password,
            uuid=new_user_dto.uuid,
        )
        new_user.create()

    def find(self, uuid: str | None) -> UserRepositoryDto:
        user = UserModel.retrieve(uuid)
        if user is None:
            raise UserNotFoundException()
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            is_admin=user.is_admin,
            uuid=str(user.uuid),
        )

    def find_by_cpf(self, cpf: str) -> UserRepositoryDto:
        user = UserModel.retrieve_by_column("cpf", cpf)
        if user is None:
            raise UserNotFoundException()
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            is_admin=user.is_admin,
            uuid=str(user.uuid),
        )

    def find_by_email(self, email: str) -> UserRepositoryDto:
        user = UserModel.retrieve_by_column("email", email)
        if user is None:
            raise UserNotFoundException()
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            is_admin=user.is_admin,
            uuid=str(user.uuid),
        )

    def list(self) -> list[UserRepositoryDto]:
        users = UserModel.list()

        if users is None:
            return []

        return [
            UserRepositoryDto(
                cpf=user[0].cpf,
                email=user[0].email,
                name=user[0].name,
                password=user[0].password,
                is_admin=user[0].is_admin,
                uuid=str(user[0].uuid),
            )
            for user in users
        ]

    def update(self, updated_user_dto: UpdateUserOutputDto, password: str) -> None:
        user = UserModel.retrieve(updated_user_dto.uuid)
        if user:
            UserModel.update(
                {
                    "cpf": updated_user_dto.cpf,
                    "email": updated_user_dto.email,
                    "name": updated_user_dto.name,
                    "password": password,
                    "uuid": updated_user_dto.uuid,
                    "id": user.id,
                }
            )
