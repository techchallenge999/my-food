from src.domain.shared.exceptions.payment import PaymentNotFoundException
from src.infrastructure.postgresql.models.payment import PaymentModel
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryDto,
    PaymentRepositoryInterface,
)


class PaymentRepository(PaymentRepositoryInterface):
    def create(self, new_payment_dto):
        new_payment = PaymentModel(
            order_uuid=new_payment_dto.order_uuid,
            status=new_payment_dto.status,
            uuid=new_payment_dto.uuid,
        )
        new_payment.create()

    def find(self, uuid):
        payment = PaymentModel.retrieve(uuid)
        if payment is None:
            return None
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def find_by_order(self, order_uuid):
        payment = PaymentModel.retrieve_by_column("order_uuid", order_uuid)
        if payment is None:
            raise PaymentNotFoundException()
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def list(self):
        payments = PaymentModel.list()

        if payments is None:
            return []

        return [
            PaymentRepositoryDto(
                order_uuid=str(payment[0].uuid),
                status=payment[0].status,
                uuid=str(payment[0].uuid),
            )
            for payment in payments
        ]

    def update(self, update_order_dto):
        payment = PaymentModel.retrieve(update_order_dto.uuid)
        if payment is None:
            raise PaymentNotFoundException()
        PaymentModel.update({"status": update_order_dto.status})
