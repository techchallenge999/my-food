from fastapi import FastAPI
from my_food.application.use_cases.user import create_usuario, find_usuario
from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.use_cases.user.create.create_usuario_dto import (
    CreateUserInputDto,
)
from my_food.application.use_cases.user.find.find_usuario_dto import FindUserInputDto


app = FastAPI()


@app.get("/create/{name}")
async def create_user(name: str):
    repository = UserRepository()
    create_use_case = create_usuario.CreateUserUseCase(repository)
    user = create_use_case.execute(
        CreateUserInputDto(
            cpf="218.232.250-71",
            email="email@email.com",
            name=name,
            password="password123",
        )
    )
    return user


@app.get("/get/{uuid}")
async def get_user(uuid: str):
    repository = UserRepository()
    create_use_case = find_usuario.FindUserUseCase(repository)
    user = create_use_case.execute(FindUserInputDto(uuid=uuid))
    return user
