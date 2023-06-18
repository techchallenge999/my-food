from fastapi import FastAPI
from my_food.application.domain.aggregates.user.entities.user import User


app = FastAPI()


@app.get('/{name}')
async def root(name: str):
    user = User('325.021.298-93', 'email@sample.com', name, '515165164516')
    return f'Olá user {user.name}'
