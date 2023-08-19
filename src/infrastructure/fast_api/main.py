from fastapi import FastAPI
from src.infrastructure.fast_api.__init_db__ import init_db
from src.infrastructure.fast_api.views.auth import router as auth_router
from src.infrastructure.fast_api.views.user import router as users_router
from src.infrastructure.fast_api.views.product import router as products_router
from src.infrastructure.fast_api.views.order import router as orders_router
from src.infrastructure.fast_api.views.payment import router as payment_router


app = FastAPI()
app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(payment_router, prefix="/payment", tags=["Payment"])

init_db()
