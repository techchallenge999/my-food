from fastapi import APIRouter, HTTPException, status as status_code


from src.infrastructure.postgresql.repositories.order.order import OrderRepository
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.shared.errors.exceptions.base import DomainException
from src.use_cases.payment.create.create_payment import (
    CreatePaymentUseCase,
)
from src.use_cases.payment.create.create_payment_dto import (
    CreatePaymentInputDto,
    CreatePaymentOutputDto,
)


router = APIRouter()


@router.post("/", status_code=201)
async def pay_order(input_data: CreatePaymentInputDto) -> CreatePaymentOutputDto:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()
        create_use_case = CreatePaymentUseCase(
            order_repository, product_repository, user_repository
        )
        payment = create_use_case.execute(input_data)
        return payment
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
