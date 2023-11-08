from dataclasses import asdict
from typing import Annotated
import json

from fastapi import Depends

from src.infrastructure.boto.config import session
from src.infrastructure.fast_api.utils.auth import oauth2_scheme
from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationInputDto,
    AuthorizationMicroserviceInterface,
)


class AuthorizationMicroservice(AuthorizationMicroserviceInterface):
    @staticmethod
    def authorize(token: Annotated[str, Depends(oauth2_scheme)]):
        client = session.client("lambda")
        response = client.invoke(
            FunctionName="authorize",
            Payload=json.dumps(asdict(AuthorizationInputDto(token=token))),
        )
        return response
