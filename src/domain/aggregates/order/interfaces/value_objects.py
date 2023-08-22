from enum import Enum

from src.domain.shared.exceptions.order import OrderStatusProgressionNotAllowedException


class OrderStatus(Enum):
    CANCELED = "cancelado"
    PENDING_PAYMENT = "pagamento pendente"
    RECEIVED = "recebido"
    PREPARING = "preparando"
    READY = "pronto"
    WITHDRAWN = "retirado"

    def next(self):
        members = list(self.__class__)
        current_index = members.index(self)
        if members[current_index] in {members[0], members[-1]}:
            raise OrderStatusProgressionNotAllowedException()
        return members[current_index + 1]
