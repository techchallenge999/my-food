from dataclasses import dataclass


@dataclass
class UserRepositoryDto:
    password: str
    cpf: str
    email: str
    name: str
    uuid: str
