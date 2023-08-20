from abc import ABC, abstractmethod
from src.domain.shared.interfaces.validator import ValidatorInterface


class CpfInterface(ABC):
    _value: str

    @property
    @abstractmethod
    def value(self) -> str:
        pass

    @value.setter
    @abstractmethod
    def value(self, value: str):
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass


class EmailInterface(ABC):
    _value: str

    @property
    @abstractmethod
    def value(self) -> str:
        pass

    @value.setter
    @abstractmethod
    def value(self, value: str):
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
