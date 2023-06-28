from dataclasses import dataclass
from my_food.application.domain.aggregates.order.entities.order import OrderStatus
from my_food.application.use_cases.product.find.find_product_dto import FindProductOutputDto


@dataclass
class CreateOrderItemInputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class CreateOrderItemOutputDto:
    comment: str
    product: FindProductOutputDto
    quantity: int


@dataclass
class CreateOrderInputDto:
    items: list[CreateOrderItemInputDto]


@dataclass
class CreateOrderOutputDto:
    items: list[CreateOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    uuid: str
