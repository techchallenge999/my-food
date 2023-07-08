from dataclasses import dataclass


@dataclass
class ListUserOutputDto:
    cpf: str
    email: str
    name: str
    is_admin: bool
    uuid: str
