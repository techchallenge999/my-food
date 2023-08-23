from src.interface_adapters.gateways.payment_gateways import (
    PaymentGatewayInterface,
    PaymentGatewayInputDto,
    PaymentGatewayOutputDto,
)


class PaymentGateway(PaymentGatewayInterface):
    def create(self, pagamento: PaymentGatewayInputDto) -> PaymentGatewayOutputDto:
        return PaymentGatewayOutputDto(
            order_uuid=pagamento.uuid, qr_data="mocked-qr-data"
        )
