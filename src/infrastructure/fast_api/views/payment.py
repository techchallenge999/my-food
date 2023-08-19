from fastapi import APIRouter, HTTPException, status as status_code
from src.infrastructure.postgresql.repositories.order.order import OrderRepository
from src.infrastructure.postgresql.repositories.payment.payment import PaymentRepository
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.shared.exceptions.base import DomainException
from src.interface_adapters.controllers.payment import PaymentController
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)
from src.use_cases.payment.find.find_payment_dto import FindPaymentOutputDto
from src.use_cases.payment.update.update_payment_dto import (
    UpdatePaymentInputDto,
    UpdatePaymentOutputDto,
)


router = APIRouter()


@router.post("/", status_code=201)
async def checkout(input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
    try:
        return PaymentController().checkout(
            input_data, OrderRepository(), ProductRepository(), UserRepository()
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get(
    "/payment_status/{order_uuid}/",
    status_code=200,
    response_model=FindPaymentOutputDto | None,
)
async def get_payment_status(order_uuid: str):
    try:
        return PaymentController().get_payment_status(order_uuid, PaymentRepository())
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/webhook/", status_code=201, response_model=UpdatePaymentOutputDto | None)
async def webhook(input_data: UpdatePaymentInputDto):
    try:
        return PaymentController().webhook(
            input_data, PaymentRepository(), OrderRepository()
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )