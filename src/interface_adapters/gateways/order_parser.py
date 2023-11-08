from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.use_cases.order.create.create_order_dto import CreateOrderInputDto


class CreateOrderParser:
    def get_order_input_dto(
        self,
        input_data: CreateOrderInputDto,
        current_user: AuthorizationOutputDto,
    ) -> CreateOrderInputDto:
        return CreateOrderInputDto(items=input_data.items, user_uuid=current_user.uuid)
