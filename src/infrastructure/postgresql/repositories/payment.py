from src.domain.shared.exceptions.payment import PaymentNotFoundException
from src.infrastructure.postgresql.models.payment import PaymentModel
from src.interface_adapters.gateways.repositories.payment import (
    PaymentRepositoryDto,
    PaymentRepositoryInterface,
)
from src.use_cases.payment.create.create_payment_dto import CreatePaymentOutputDto
from src.use_cases.payment.update.update_payment_dto import UpdatePaymentOutputDto


class PaymentRepository(PaymentRepositoryInterface):
    def create(self, new_payment_dto: CreatePaymentOutputDto) -> None:
        new_payment = PaymentModel(
            order_uuid=new_payment_dto.order_uuid,
            status=new_payment_dto.status,
            uuid=new_payment_dto.uuid,
        )
        new_payment.create()

    def find(self, uuid: str) -> PaymentRepositoryDto:
        payment = PaymentModel.retrieve(uuid)
        if payment is None:
            raise PaymentNotFoundException()
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def find_by_order(self, order_uuid: str) -> PaymentRepositoryDto | None:
        payment = PaymentModel.retrieve_by_column("order_uuid", order_uuid)
        if payment is None:
            raise PaymentNotFoundException()
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def list(self) -> list[PaymentRepositoryDto]:
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

    def update(self, updated_order_dto: UpdatePaymentOutputDto) -> None:
        payment = PaymentModel.retrieve(updated_order_dto.uuid)
        if payment:
            PaymentModel.update({"status": updated_order_dto.status})
