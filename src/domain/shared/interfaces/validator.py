from abc import ABC, abstractmethod


class ValidatorInterface(ABC):
    @abstractmethod
    def __init__(self, domain_object: ABC):
        pass

    @abstractmethod
    def validate(self) -> None:
        pass
