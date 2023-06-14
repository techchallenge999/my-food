from abc import abstractmethod
from my_food.application.domain.compartilhado.repository.abstract_repository import (
    RepositoryInterface,
)
from my_food.application.domain.usuarios.Interfaces.usuario import UsuarioAbstrato


class UserRepository(RepositoryInterface):
    @abstractmethod
    def create(self, entity: UsuarioAbstrato) -> None:
        pass

    @abstractmethod
    def find(self, id: str) -> UsuarioAbstrato:
        pass

    @abstractmethod
    def find_all(self) -> list[UsuarioAbstrato]:
        pass

    @abstractmethod
    def update(self, entity: UsuarioAbstrato) -> None:
        pass
