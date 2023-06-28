from dataclasses import asdict
from typing import List, Optional
from my_food.application.domain.aggregates.order.interfaces.order_repository import OrderRepositoryInterface
from my_food.application.use_cases.order.find.find_order_dto import FindOrderItemOutputDto, FindOrderOutputDto


class ListOrderUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(self) -> Optional[List[FindOrderOutputDto]]:
        orders_list = self._repository.list()

        if orders_list is None:
            return None

        return [
            FindOrderOutputDto(
                items=[FindOrderItemOutputDto(**asdict(item)) for item in order.items],
                status=order.status,
                total_amount=order.total_amount,
                uuid=order.uuid,
            )
            for order in orders_list
        ]
