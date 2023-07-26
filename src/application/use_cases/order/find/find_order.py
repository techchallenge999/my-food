from dataclasses import asdict

from src.application.domain.aggregates.order.interfaces.order_repository import (
    OrderRepositoryInterface,
)
from src.application.domain.shared.errors.exceptions.order import (
    OrderNotFoundException,
)
from src.application.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderItemOutputDto,
    FindOrderOutputDto,
)


class FindOrderUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindOrderInputDto) -> FindOrderOutputDto:
        order = self._repository.find(uuid=input_data.uuid)

        if order is None:
            raise OrderNotFoundException()

        return FindOrderOutputDto(
            items=[FindOrderItemOutputDto(**asdict(item)) for item in order.items],
            status=order.status,
            total_amount=order.total_amount,
            user_uuid=order.user_uuid,
            uuid=order.uuid,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
