from fastapi import FastAPI
from my_food.adapters.FastAPI.views.auth import router as auth_router
from my_food.adapters.FastAPI.views.user import router as users_router
from my_food.adapters.FastAPI.views.product import router as products_router
from my_food.adapters.FastAPI.views.order import router as orders_router


app = FastAPI()
app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
