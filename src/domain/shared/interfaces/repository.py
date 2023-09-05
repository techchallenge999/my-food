from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, entity_dto: ABC) -> None:
        pass

    @abstractmethod
    def list(self, uuid: str) -> ABC:
        pass

    @abstractmethod
    def find(self, uuid: str) -> ABC:
        pass

    @abstractmethod
    def update(self, entity_dto: ABC) -> None:
        pass
