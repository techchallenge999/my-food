from fastapi import FastAPI
from my_food.adapters.FastAPI.views.auth import router


app = FastAPI()
app.include_router(router)
