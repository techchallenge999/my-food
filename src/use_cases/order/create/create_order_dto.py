from dataclasses import dataclass

from src.domain.aggregates.order.value_objects.order_status import OrderStatus


@dataclass
class CreateOrderItemInputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class CreateOrderItemOutputDto:
    comment: str
    product_uuid: str
    quantity: int


@dataclass
class CreateOrderInputDto:
    items: list[CreateOrderItemInputDto]
    user_uuid: str | None = None


@dataclass
class CreateOrderOutputDto:
    items: list[CreateOrderItemOutputDto]
    status: OrderStatus
    total_amount: str
    user_uuid: str | None
    uuid: str
