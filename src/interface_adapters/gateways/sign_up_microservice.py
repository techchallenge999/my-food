from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SignUpInputDto:
    cpf: str
    is_admin: bool
    password: str
    uuid: str


class SignUpMicroserviceInterface(ABC):
    @abstractmethod
    def save(self, sign_up_input_dto: SignUpInputDto) -> None:
        pass
