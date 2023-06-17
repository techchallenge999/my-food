from abc import ABC, abstractmethod
from typing import TypeVar


GenericEntity = TypeVar('GenericEntity')


class InterfaceValidator(ABC):
    @abstractmethod
    def __init__(self, entity: GenericEntity) -> None:
        pass

    @abstractmethod
    def validate(self) -> None:
        pass
