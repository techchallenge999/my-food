from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.shared.exceptions.order import (
    OrderNotFoundException,
)
from src.use_cases.order.delete.delete_order_dto import (
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
            items=[
                DeleteOrderItemOutputDto(
                    comment=item.comment,
                    product_uuid=item.product.uuid,
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=order.status,
            total_amount=order.total_amount,
            user_uuid=order.user_uuid,
            uuid=order.uuid,
        )
