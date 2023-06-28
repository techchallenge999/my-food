from dataclasses import asdict
from typing import Optional

from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.use_cases.order.find.find_order_dto import FindOrderInputDto, FindOrderItemOutputDto, FindOrderOutputDto


class FindOrderUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(self, input_data: FindOrderInputDto) -> Optional[FindOrderOutputDto]:
        order = self._repository.find(uuid=input_data.uuid)

        if order is None:
            return None

        return FindOrderOutputDto(
            items=[FindOrderItemOutputDto(**asdict(item)) for item in order.items],
            status=order.status,
            total_amount=order.total_amount,
            uuid=order.uuid,
        )
