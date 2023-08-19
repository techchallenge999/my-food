from src.interface_adapters.gateways.auth import EmptyUser
from src.use_cases.order.create.create_order_dto import CreateOrderInputDto
from src.use_cases.user.find.find_user_dto import FindUserOutputDto


class CreateOrderParser:
    def get_dto(
        self,
        input_data: CreateOrderInputDto,
        current_user: FindUserOutputDto | EmptyUser,
    ) -> CreateOrderInputDto:
        return CreateOrderInputDto(items=input_data.items, user_uuid=current_user.uuid)
