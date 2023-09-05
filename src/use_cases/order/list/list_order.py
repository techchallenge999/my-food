from dataclasses import asdict

from src.domain.aggregates.order.value_objects.order_status import OrderStatus
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

    def execute(self) -> list[ListOrderOutputDto]:
        exclusive_filters = {
            "status": [
                OrderStatus.PENDING_PAYMENT,
                OrderStatus.CANCELED,
                OrderStatus.WITHDRAWN,
            ]
        }
        order_list = self._repository.list(exclusive_filters=exclusive_filters)

        if order_list is None:
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
            for order in order_list
        ]
