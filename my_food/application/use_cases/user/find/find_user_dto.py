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


@dataclass
class FindUserByCpfInputDto:
    cpf: str


@dataclass
class FindUserByCpfOutputDto:
    cpf: str
    email: str
    name: str
    password: str
    uuid: str
