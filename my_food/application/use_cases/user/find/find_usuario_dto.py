from dataclasses import dataclass


@dataclass
class FindUserInputDto:
    uuid: str


@dataclass
class FindUserOutputDto:
    cpf: str
    email: str
    name: str
    uuid: str
