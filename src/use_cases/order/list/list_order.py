from dataclasses import asdict
from typing import List, Optional
from src.domain.aggregates.order.interfaces.order_entity import OrderStatus

from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.use_cases.order.list.list_order_dto import (
    ListOrderItemOutputDto,
    ListOrderOutputDto,
)


class ListOrderUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(
        self, filters: dict | None = None
    ) -> Optional[List[ListOrderOutputDto]]:
        orders_list = self._repository.list(filters=filters)

        if orders_list is None:
            return []

        return [
            ListOrderOutputDto(
                items=[ListOrderItemOutputDto(**asdict(item)) for item in order.items],
                status=order.status,
                total_amount=order.total_amount,
                user_uuid=order.user_uuid,
                uuid=order.uuid,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
            for order in orders_list
        ]


class ListAllButWithdrawOrdersUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def execute(self) -> Optional[List[ListOrderOutputDto]]:
        exclusive_filters = {"status": OrderStatus.WITHDRAWN}
        orders_list = self._repository.list(exclusive_filters=exclusive_filters)

        if orders_list is None:
            return []

        return [
            ListOrderOutputDto(
                items=[ListOrderItemOutputDto(**asdict(item)) for item in order.items],
                status=order.status,
                total_amount=order.total_amount,
                user_uuid=order.user_uuid,
                uuid=order.uuid,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
            for order in orders_list
        ]
