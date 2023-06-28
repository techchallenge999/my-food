from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatusCategory
from my_food.application.use_cases.product.find.find_product_dto import FindProductOutputDto


@dataclass
class UpdateOrderItemInputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class UpdateOrderItemOutputDto:
    comment: str
    product: FindProductOutputDto
    quantity: int


@dataclass
class UpdateOrderInputDto:
    items: list[UpdateOrderItemInputDto]
    status: OrderStatusCategory
    uuid: str


@dataclass
class UpdateOrderOutputDto:
    items: list[UpdateOrderItemOutputDto]
    status: OrderStatusCategory
    total_amount: str
    uuid: str
