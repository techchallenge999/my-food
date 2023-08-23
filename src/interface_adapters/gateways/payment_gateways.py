from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentGatewayInputDto:
    uuid: str
    notification_url: str
    total_amount: str


@dataclass
class PaymentGatewayOutputDto:
    uuid: str
    qr_data: str


class PaymentGatewayInterface(ABC):
    @abstractmethod
    def create(self, payment_data: PaymentGatewayInputDto) -> PaymentGatewayOutputDto:
        pass
