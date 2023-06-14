from abc import ABC, abstractmethod
from typing import TypeVar

GenericEntity = TypeVar("GenericEntity")


class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, entity: GenericEntity) -> None:
        pass

    @abstractmethod
    def find(self, id: str) -> GenericEntity:
        pass

    @abstractmethod
    def find_all(self) -> list[GenericEntity]:
        pass

    @abstractmethod
    def update(self, entity: GenericEntity) -> None:
        pass
