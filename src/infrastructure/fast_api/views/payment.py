from fastapi import APIRouter, HTTPException, status as status_code

from src.domain.shared.exceptions.base import DomainException
from src.infrastructure.checkout.mock_checkout import PaymentGateway
from src.infrastructure.postgresql.repositories.order import OrderRepository
from src.infrastructure.postgresql.repositories.payment import PaymentRepository
from src.infrastructure.postgresql.repositories.product import ProductRepository
from src.infrastructure.postgresql.repositories.user import UserRepository
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


@router.post("/", status_code=201, response_model=CreatePaymentOutputDto)
async def checkout(input_data: CreatePaymentInputDto):
    try:
        return PaymentController(PaymentRepository(), PaymentGateway()).checkout(
            input_data, OrderRepository()
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
        return PaymentController(
            PaymentRepository(), PaymentGateway()
        ).get_payment_status(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/webhook/{payment_uuid}",
    status_code=201,
    response_model=UpdatePaymentOutputDto | None,
)
async def webhook(payment_uuid: str, input_data: UpdatePaymentInputDto):
    try:
        return PaymentController(PaymentRepository(), PaymentGateway()).webhook(
            payment_uuid,
            input_data,
            OrderRepository(),
            ProductRepository(),
            UserRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
