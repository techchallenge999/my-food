from dataclasses import dataclass
from src.use_cases.user.find.find_user_dto import FindUserByCpfInputDto


@dataclass
class EmptyUser:
    uuid: str | None = None


class FindUserParser:
    def __init__(self, cpf: str):
        self.cpf = cpf

    def get_dto(self) -> FindUserByCpfInputDto:
        return FindUserByCpfInputDto(cpf=self.cpf)

    def get_actor_cpf(self) -> str:
        return self.cpf
