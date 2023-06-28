from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatusCategory
from my_food.application.use_cases.product.find.find_product_dto import FindProductOutputDto


@dataclass
class FindOrderItemOutputDto:
    comment: str
    product: FindProductOutputDto
    quantity: int


class FindOrderInputDto:
    uuid: str


@dataclass
class FindOrderOutputDto:
    items: list[FindOrderItemOutputDto]
    status: OrderStatusCategory
    total_amount: str
    uuid: str
