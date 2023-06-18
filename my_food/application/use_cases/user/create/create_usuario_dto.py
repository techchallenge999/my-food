from dataclasses import dataclass


@dataclass
class CreateUserInputDto:
    cpf: str
    email: str
    name: str
    password: str


@dataclass
class CreateUserOutputDto:
    cpf: str
    email: str
    name: str
    uuid: str
