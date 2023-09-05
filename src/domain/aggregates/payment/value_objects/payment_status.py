from enum import Enum


class PaymentStatus(Enum):
    PENDING = "pendente"
    PAID = "pago"
    REFUSED = "recusado"
