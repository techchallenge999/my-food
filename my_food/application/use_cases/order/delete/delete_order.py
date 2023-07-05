from dataclasses import asdict

from my_food.application.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from my_food.application.domain.shared.errors.exceptions.order import (
    OrderNotFoundException,
)
from my_food.application.use_cases.order.delete.delete_order_dto import (
    DeleteOrderInputDto,
    DeleteOrderItemOutputDto,
    DeleteOrderOutputDto,
)


class DeleteOrderUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: DeleteOrderInputDto) -> DeleteOrderOutputDto:
        order = self._repository.find(uuid=input_data.uuid)

        if order is None:
            raise OrderNotFoundException()

        self._repository.delete(uuid=order.uuid)

        return DeleteOrderOutputDto(
            items=[DeleteOrderItemOutputDto(**asdict(item)) for item in order.items],
            status=order.status,
            total_amount=order.total_amount,
            user_uuid=order.user_uuid,
            uuid=order.uuid,
        )
