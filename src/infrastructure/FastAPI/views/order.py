from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, status as status_code, Depends
from src.infrastructure.FastAPI.utils.auth import get_current_user_optional
from src.infrastructure.FastAPI.utils.schemas import CreateOrderSchema

from src.infrastructure.postgresql.repositories.order.order import OrderRepository
from src.infrastructure.postgresql.repositories.product.product import ProductRepository
from src.infrastructure.postgresql.repositories.user.user import UserRepository
from src.domain.aggregates.order.interfaces.order_entity import (
    OrderStatus,
)
from src.domain.shared.exceptions.base import DomainException
from src.interface_adapters.presenters.auth import EmptyUser
from src.use_cases.order.create.create_order import CreateOrderUseCase
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from src.use_cases.order.delete.delete_order import DeleteOrderUseCase
from src.use_cases.order.delete.delete_order_dto import (
    DeleteOrderInputDto,
    DeleteOrderOutputDto,
)
from src.use_cases.order.find.find_order import FindOrderUseCase
from src.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderOutputDto,
)
from src.use_cases.order.list.list_order import ListOrderUseCase
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order import UpdateOrderUseCase
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderInputDto,
    UpdateOrderItemInputDto,
    UpdateOrderOutputDto,
    UpdateStatusOrderInputDto,
)
from src.use_cases.user.find.find_user_dto import FindUserOutputDto


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
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/", status_code=200)
async def list_orders(status: str | None = None) -> Optional[List[ListOrderOutputDto]]:
    try:
        repository = OrderRepository()
        list_use_case = ListOrderUseCase(repository)
        filters = {}
        if status is not None:
            filters["status"] = OrderStatus(status).name
        orders = list_use_case.execute(filters)
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
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
            status_code=status_code.HTTP_400_BAD_REQUEST,
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
            status_code=status_code.HTTP_400_BAD_REQUEST,
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
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/{order_uuid}/update-status/", status_code=200)
async def update_status_order(
    input_data: UpdateStatusOrderInputDto,
    order_uuid: str,
) -> Optional[UpdateOrderOutputDto]:
    try:
        order_repository = OrderRepository()
        product_repository = ProductRepository()
        user_repository = UserRepository()

        find_use_case = FindOrderUseCase(order_repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        order = UpdateOrderInputDto(
            items=[
                UpdateOrderItemInputDto(
                    comment=item.comment,
                    product_uuid=item.product["uuid"],
                    quantity=item.quantity,
                )
                for item in order.items
            ],
            status=input_data.status,
            uuid=order.uuid,
        )

        update_use_case = UpdateOrderUseCase(
            order_repository, product_repository, user_repository
        )
        orders = update_use_case.execute(order)
        return orders
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
