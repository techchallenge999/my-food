from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, status as status_code, Depends
from src.infrastructure.fast_api.utils.auth import EmptyUser, get_current_user_optional
from src.infrastructure.postgresql.repositories.order.order import OrderRepository
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.shared.exceptions.base import DomainException
from src.interface_adapters.controllers.order import OrderController
from src.interface_adapters.gateways.order import CreateOrderParser
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from src.use_cases.order.delete.delete_order_dto import DeleteOrderOutputDto
from src.use_cases.order.find.find_order_dto import FindOrderOutputDto
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderOutputDto,
    UpdateStatusOrderInputDto,
)
from src.use_cases.user.find.find_user_dto import FindUserOutputDto


router = APIRouter()


@router.post("/", status_code=201)
async def create_order(
    input_data: CreateOrderInputDto,
    current_user: Annotated[
        FindUserOutputDto | EmptyUser, Depends(get_current_user_optional)
    ],
) -> CreateOrderOutputDto:
    try:
        return OrderController(OrderRepository()).create_order(
            input_data,
            CreateOrderParser(),
            ProductRepository(),
            UserRepository(),
            current_user,
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/", status_code=200)
async def list_all_but_withdrawn_orders() -> Optional[List[ListOrderOutputDto]]:
    try:
        return OrderController(OrderRepository()).list_all_but_withdrawn()
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/", status_code=200)
async def update_order(
    input_data: UpdateOrderInputDto,
) -> Optional[UpdateOrderOutputDto]:
    try:
        return OrderController(OrderRepository()).update_order(
            input_data,
            ProductRepository(),
            UserRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{order_uuid}/", status_code=200, response_model=FindOrderOutputDto)
async def retireve_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).retireve_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{order_uuid}/", status_code=200, response_model=DeleteOrderOutputDto)
async def delete_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).delete_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/{order_uuid}/update-status/", status_code=200)
async def update_order_status(
    order_uuid: str,
    input_data: UpdateStatusOrderInputDto,
) -> UpdateOrderOutputDto:
    try:
        return OrderController(OrderRepository()).update_order_status(
            order_uuid,
            input_data,
            ProductRepository(),
            UserRepository(),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
