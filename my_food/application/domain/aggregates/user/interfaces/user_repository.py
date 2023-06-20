from abc import abstractmethod
from typing import Optional
from my_food.application.domain.aggregates.user.interfaces.user_dto import (
    UserRepositoryDto,
)

from my_food.application.domain.aggregates.user.interfaces.user_entity import (
    UserInterface,
)
from my_food.application.domain.shared.interfaces.repository import RepositoryInterface


class UserRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: UserInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[UserRepositoryDto]:
        pass

    @abstractmethod
    def update(self, entity: UserInterface) -> None:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[UserRepositoryDto]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserRepositoryDto]:
        pass
