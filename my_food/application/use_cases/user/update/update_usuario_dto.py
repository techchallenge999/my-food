from dataclasses import dataclass


@dataclass
class UpdateUserInputDto:
    cpf: str
    email: str
    name: str
    uuid: str


@dataclass
class UpdateUserOutputDto:
    cpf: str
    email: str
    name: str
    uuid: str
