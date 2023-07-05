from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from my_food.adapters.postgresql.repositories.order.order import OrderRepository
from my_food.adapters.postgresql.repositories.product.product import ProductRepository
from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.domain.shared.errors.exceptions.base import DomainException
from my_food.application.use_cases.order.create.create_order import CreateOrderUseCase
from my_food.application.use_cases.order.create.create_order_dto import CreateOrderInputDto, CreateOrderOutputDto
from my_food.application.use_cases.order.list.list_order import ListOrderUseCase
from my_food.application.use_cases.order.list.list_order_dto import ListOrderOutputDto
from my_food.application.use_cases.order.update.update_order import UpdateOrderUseCase
from my_food.application.use_cases.order.update.update_order_dto import UpdateOrderInputDto, UpdateOrderOutputDto


router = APIRouter()


@router.post('/create-order', status_code=201)
async def create_order(input_data: CreateOrderInputDto) -> CreateOrderOutputDto:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()
        create_use_case = CreateOrderUseCase(order_repository, product_repository, user_repository)
        new_user = create_use_case.execute(CreateOrderInputDto(items=input_data.items, user_uuid=input_data.user_uuid))
        return new_user
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/list-orders', status_code=200)
async def list_orders() -> Optional[List[ListOrderOutputDto]]:
    try:
        repository = OrderRepository()
        list_use_case = ListOrderUseCase(repository)
        orders = list_use_case.execute()
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/update-orders', status_code=200)
async def update_orders(input_data: UpdateOrderInputDto) -> Optional[UpdateOrderOutputDto]:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()
        update_use_case = UpdateOrderUseCase(order_repository, product_repository, user_repository)
        orders = update_use_case.execute(input_data)
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
