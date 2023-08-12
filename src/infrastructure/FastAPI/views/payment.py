from fastapi import APIRouter, HTTPException, status as status_code
from src.infrastructure.postgresql.repositories.order.order import OrderRepository
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.shared.exceptions.base import DomainException
from src.interface_adapters.controllers.payment import PaymentController
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)


router = APIRouter()


@router.post("/", status_code=201)
async def pay_order(input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
    try:
        return PaymentController(
            OrderRepository(), ProductRepository(), UserRepository()
        ).pay_order(input_data)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
