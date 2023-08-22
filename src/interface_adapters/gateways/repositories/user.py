from abc import abstractmethod
from dataclasses import dataclass

from src.domain.aggregates.user.interfaces.entities import (
    UserInterface,
)
from src.domain.shared.interfaces.repository import RepositoryInterface


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
    def find(self, uuid: str | None) -> UserRepositoryDto | None:
        pass

    @abstractmethod
    def list(self) -> list[UserRepositoryDto]:
        pass

    @abstractmethod
    def update(self, entity: UserInterface) -> None:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> UserRepositoryDto | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserRepositoryDto | None:
        pass
