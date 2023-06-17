from fastapi import FastAPI
from my_food.application.domain.agregado_usuario.entities.usuario import Usuario


app = FastAPI()


@app.get('/{nome}')
async def root(nome: str):
    usuario = Usuario('325.021.298-93', 'email@sample.com', nome, '515165164516')
    return f'Olá user {usuario.nome}'
