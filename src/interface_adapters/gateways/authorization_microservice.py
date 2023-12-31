from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthorizationInputDto:
    token: str


@dataclass
class AuthorizationOutputDto:
    is_admin: bool
    uuid: str


class AuthorizationMicroserviceInterface(ABC):
    @staticmethod
    @abstractmethod
    def authorize(
        authorization_input_dto: AuthorizationInputDto,
    ) -> AuthorizationOutputDto:
        pass
