from abc import ABC, abstractmethod
from typing import TypeVar


GenericEntity = TypeVar('GenericEntity')


class ValidatorInterface(ABC):
    @abstractmethod
    def __init__(self, entity: GenericEntity):
        pass

    @abstractmethod
    def validate(self) -> None:
        pass
