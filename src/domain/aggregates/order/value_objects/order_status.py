from enum import Enum

from src.domain.shared.exceptions.order import OrderStatusProgressionNotAllowedException


class OrderStatus(Enum):
    CANCELED = "canceled"
    PENDING_PAYMENT = "pending_payment"
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    WITHDRAWN = "withdrawn"

    def next(self) -> "OrderStatus":
        members = list(self.__class__)
        current_index = members.index(self)
        if members[current_index] in {members[0], members[-1]}:
            raise OrderStatusProgressionNotAllowedException()
        return members[current_index + 1]
