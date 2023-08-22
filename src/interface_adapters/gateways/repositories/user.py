from abc import abstractmethod
from dataclasses import dataclass

from src.domain.shared.interfaces.repository import RepositoryInterface
from src.use_cases.user.create.create_user_dto import CreateUserOutputDto
from src.use_cases.user.update.update_user_dto import UpdateUserOutputDto


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
    def create(self, new_user_dto: CreateUserOutputDto, password: str) -> None:
        pass

    @abstractmethod
    def find(self, uuid: str | None) -> UserRepositoryDto:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> UserRepositoryDto:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserRepositoryDto:
        pass

    @abstractmethod
    def list(self) -> list[UserRepositoryDto]:
        pass

    @abstractmethod
    def update(self, updated_user_dto: UpdateUserOutputDto, password: str) -> None:
        pass
