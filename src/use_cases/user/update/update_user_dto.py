from dataclasses import dataclass


@dataclass
class UpdateUserInputDto:
    email: str
    name: str
    uuid: str


@dataclass
class UpdateUserOutputDto:
    cpf: str
    email: str
    name: str
    is_admin: bool
    uuid: str
