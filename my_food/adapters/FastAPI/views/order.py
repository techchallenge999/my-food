from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, status, Request, Depends
from my_food.adapters.FastAPI.utils.auth import get_current_user_optional
from my_food.adapters.FastAPI.utils.schemas import CreateOrderSchema, EmptyUser

from my_food.adapters.postgresql.repositories.order.order import OrderRepository
from my_food.adapters.postgresql.repositories.product.product import ProductRepository
from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.domain.shared.errors.exceptions.base import DomainException
from my_food.application.use_cases.order.create.create_order import CreateOrderUseCase
from my_food.application.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from my_food.application.use_cases.order.delete.delete_order import DeleteOrderUseCase
from my_food.application.use_cases.order.delete.delete_order_dto import (
    DeleteOrderInputDto,
    DeleteOrderOutputDto,
)
from my_food.application.use_cases.order.find.find_order import FindOrderUseCase
from my_food.application.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderOutputDto,
)
from my_food.application.use_cases.order.list.list_order import ListOrderUseCase
from my_food.application.use_cases.order.list.list_order_dto import ListOrderOutputDto
from my_food.application.use_cases.order.update.update_order import UpdateOrderUseCase
from my_food.application.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderOutputDto,
)
from my_food.application.use_cases.user.find.find_user_dto import FindUserOutputDto


router = APIRouter()


@router.post("/", status_code=201)
async def create_order(
    input_data: CreateOrderSchema,
    current_user: Annotated[
        FindUserOutputDto | EmptyUser, Depends(get_current_user_optional)
    ],
) -> CreateOrderOutputDto:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()
        user_uuid = current_user.uuid if current_user else None
        create_use_case = CreateOrderUseCase(
            order_repository, product_repository, user_repository
        )
        new_user = create_use_case.execute(
            CreateOrderInputDto(items=input_data.items, user_uuid=user_uuid)
        )
        return new_user
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/", status_code=200)
async def list_orders(request: Request) -> Optional[List[ListOrderOutputDto]]:
    try:
        repository = OrderRepository()
        list_use_case = ListOrderUseCase(repository)
        filters = request.query_params._dict
        orders = list_use_case.execute(filters)
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/", status_code=200)
async def update_orders(
    input_data: UpdateOrderInputDto,
) -> Optional[UpdateOrderOutputDto]:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()
        update_use_case = UpdateOrderUseCase(
            order_repository, product_repository, user_repository
        )
        orders = update_use_case.execute(input_data)
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{order_uuid}/", status_code=200, response_model=FindOrderOutputDto)
async def retireve_order(order_uuid: str):
    try:
        repository = OrderRepository()
        find_use_case = FindOrderUseCase(repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        return order
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{order_uuid}/", status_code=200, response_model=DeleteOrderOutputDto)
async def delete_order(order_uuid: str):
    try:
        repository = OrderRepository()
        delete_use_case = DeleteOrderUseCase(repository)
        order = delete_use_case.execute(DeleteOrderInputDto(uuid=order_uuid))
        return order
    except DomainException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
