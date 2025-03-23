from fastapi import FastAPI

# HTTP (FastAPI) Routers
from app.adapters.http.customer_api import router as customer_router
from app.adapters.http.orders_api import router as order_router
from app.adapters.http.products_api import router as product_router

app = FastAPI()

app.include_router(
    customer_router,
    prefix="/customers",
    tags=["customers"],
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["orders"],
)

app.include_router(
    product_router,
    prefix="/products",
    tags=["products"],
)
