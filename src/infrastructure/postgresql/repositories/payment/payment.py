from typing import List, Optional
from src.domain.aggregates.payment.interfaces.payment_entity import PaymentInterface
from src.domain.aggregates.payment.interfaces.payment_repository import (
    PaymentRepositoryDto,
    PaymentRepositoryInterface,
)
from src.domain.shared.exceptions.payment import PaymentNotFoundException
from src.infrastructure.postgresql.models.payment.payment import PaymentModel


class PaymentRepository(PaymentRepositoryInterface):
    def create(self, entity: PaymentInterface) -> None:
        new_payment = PaymentModel(
            order_uuid=entity.order_uuid,
            status=entity.status,
            uuid=entity.uuid,
        )
        new_payment.create()

    def find(self, uuid: str) -> Optional[PaymentRepositoryDto]:
        payment = PaymentModel.retrieve(uuid)
        if payment is None:
            raise PaymentNotFoundException()
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def find_by_order(self, order_uuid: str) -> Optional[PaymentRepositoryDto]:
        payment = PaymentModel.retrieve_by_column("order_uuid", order_uuid)
        if payment is None:
            raise PaymentNotFoundException()
        return PaymentRepositoryDto(
            order_uuid=str(payment.order_uuid),
            status=payment.status,
            uuid=str(payment.uuid),
        )

    def list(self) -> Optional[List[PaymentRepositoryDto]]:
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

    def update(self, entity: PaymentInterface) -> None:
        payment = PaymentModel.retrieve(entity.uuid)
        if payment:
            PaymentModel.update({"status": entity.status})
