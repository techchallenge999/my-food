from abc import abstractmethod
from typing import Optional
from my_food.application.domain.agregado_usuario.interfaces.entidade_usuario import InterfaceUsuario
from my_food.application.domain.compartilhado.interfaces.repositorio import InterfaceRepositorio


class InterfaceRepositorioUsuario(InterfaceRepositorio):
    @abstractmethod
    def create(self, entity: InterfaceUsuario) -> None:
        pass

    @abstractmethod
    def find(self, id_: str) -> InterfaceUsuario:
        pass

    @abstractmethod
    def update(self, entity: InterfaceUsuario) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[InterfaceUsuario]:
        pass
