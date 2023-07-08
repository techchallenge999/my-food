from dataclasses import dataclass


@dataclass
class FindUserInputDto:
    uuid: str


@dataclass
class FindUserOutputDto:
    cpf: str
    email: str
    name: str
    is_admin: bool
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
    is_admin: bool
    uuid: str
