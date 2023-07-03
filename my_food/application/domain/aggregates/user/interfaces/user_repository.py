from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from my_food.application.domain.aggregates.user.interfaces.user_entity import (
    UserInterface,
)
from my_food.application.domain.shared.interfaces.repository import RepositoryInterface


@dataclass
class UserRepositoryDto:
    cpf: str
    email: str
    name: str
    password: str
    is_admin: bool
    uuid: str


class UserRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, entity: UserInterface) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str) -> Optional[UserRepositoryDto]:
        pass

    @abstractmethod
    def list(self) -> Optional[List[UserRepositoryDto]]:
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
