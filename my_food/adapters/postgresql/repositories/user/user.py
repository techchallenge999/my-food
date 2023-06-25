from typing import Optional

from my_food.adapters.postgresql.models.user.user import UserModel
from my_food.application.domain.aggregates.user.interfaces.user_entity import (
    UserInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryDto,
    UserRepositoryInterface,
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
        new_user.save()

    def find(self, uuid: str) -> Optional[UserRepositoryDto]:
        user = UserModel.retrieve(uuid)
        if user is None:
            return None
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            uuid=str(user.uuid),
        )

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
            return None
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            uuid=str(user.uuid),
        )

    def find_by_email(self, email: str) -> Optional[UserRepositoryDto]:
        user = UserModel.retrieve_by_column("email", email)
        if user is None:
            return None
        return UserRepositoryDto(
            cpf=user.cpf,
            email=user.email,
            name=user.name,
            password=user.password,
            uuid=str(user.uuid),
        )
