from dataclasses import asdict
import json

from src.infrastructure.boto.config import session
from src.interface_adapters.gateways.sign_up_microservice import (
    SignUpMicroserviceInterface,
)


class SignUpMicroservice(SignUpMicroserviceInterface):
    def save(self, sign_up_input_dto):
        client = session.client("lambda")
        client.invoke(
            FunctionName="sign-up-save", Payload=json.dumps(asdict(sign_up_input_dto))
        )
