from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from jose import JWTError
from passlib.context import CryptContext
from typing import Annotated

from my_food.adapters.postgresql.repositories.user.user import UserRepository
from my_food.application.use_cases.user import create_user, find_user
from my_food.application.use_cases.user.create.create_user_dto import CreateUserInputDto
from my_food.application.use_cases.user.find.find_user_dto import FindUserByCpfInputDto, FindUserOutputDto

from my_food.adapters.FastAPI.auth_utils import create_access_token, raise_credentials_exception, decode_access_token
from my_food.adapters.FastAPI.schemas import TokenModel


app = FastAPI()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/register', status_code=201)
async def register(input_data: CreateUserInputDto):
    repository = UserRepository()
    create_use_case = create_user.CreateUserUseCase(repository)
    new_user = create_use_case.execute(
        CreateUserInputDto(
            cpf=input_data.cpf,
            email=input_data.email,
            name=input_data.name,
            password=input_data.password,
        )
    )
    return new_user


@app.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]):
    user = await get_user_by_cpf(form_data.username)
    if not (user and (user.password == form_data.password)):
        raise_credentials_exception('Incorrect username or password')
    access_token = create_access_token({"sub": user.cpf})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/get-by-cpf/{cpf}')
async def get_user_by_cpf(cpf: str):
    repository = UserRepository()
    find_user_by_cpf_use_case = find_user.FindUserByCpfUseCase(repository)
    user = find_user_by_cpf_use_case.execute(FindUserByCpfInputDto(cpf=cpf))
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_access_token(token)
        username: str = payload["sub"]
        if username is None:
            raise_credentials_exception('Could not validate credentials')
    except JWTError:
        raise_credentials_exception('Could not validate credentials')
    user = await get_user_by_cpf(username)
    if user is None:
        raise_credentials_exception('Could not validate credentials')
    return user


@app.get("/users/me/", response_model=FindUserOutputDto)
async def read_users_me(current_user: Annotated[FindUserOutputDto, Depends(get_current_user)]):
    return current_user
