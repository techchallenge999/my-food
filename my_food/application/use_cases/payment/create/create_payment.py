from uuid import UUID

from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.domain.aggregates.payment.entities.payment import Payment
from my_food.application.domain.aggregates.payment.interfaces.payment_repository import PaymentRepositoryInterface
from my_food.application.use_cases.payment.create.create_payment_dto import CreatePaymentInputDto, CreatePaymentOutputDto


class CreatePaymentUseCase:
    def __init__(
            self,
            payment_repository: PaymentRepositoryInterface,
            order_repository: OrderRepositoryInterface,
        ):
        self._payment_repository = payment_repository
        self._order_repository = order_repository

    def execute(self, input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
        new_payment = Payment(
            order_uuid=UUID(input_data.order_uuid),
            payment_repository=self._payment_repository,
            order_repository=self._order_repository,
        )

        self._payment_repository.create(entity=new_payment)

        return CreatePaymentOutputDto(
            order_uuid=new_payment.order_uuid,
            status=new_payment.status,
            uuid=new_payment.uuid,
        )
