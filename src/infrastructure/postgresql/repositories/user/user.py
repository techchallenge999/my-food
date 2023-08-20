from typing import List, Optional

from src.infrastructure.postgresql.models.user.user import UserModel
from src.domain.aggregates.user.interfaces.entities import (
    UserInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryDto,
    UserRepositoryInterface,
)
from src.domain.shared.exceptions.user import (
    UserNotFoundException,
)


class UserRepository(UserRepositoryInterface):
    def create(self, entity: UserInterface) -> None:
        new_user = UserModel(
            cpf=entity.cpf,
            email=entity.email,
            name=entity.name,
            password=entity.password,
            uuid=entity.uuid,
        )
        new_user.create()

    def find(self, uuid: str | None) -> Optional[UserRepositoryDto]:
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

    def list(self) -> Optional[List[UserRepositoryDto]]:
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

    def update(self, entity: UserInterface) -> None:
        user = UserModel.retrieve(entity.uuid)
        if user:
            UserModel.update(
                {
                    "cpf": entity.cpf,
                    "email": entity.email,
                    "name": entity.name,
                    "password": entity.password,
                    "uuid": entity.uuid,
                    "id": user.id,
                }
            )

    def find_by_cpf(self, cpf: str) -> Optional[UserRepositoryDto]:
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

    def find_by_email(self, email: str) -> Optional[UserRepositoryDto]:
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
