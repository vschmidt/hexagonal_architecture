import logging
from fastapi import FastAPI

from src.api.endpoints import health_check_router, orders_router, users_router


def inject_routers(app: FastAPI):
    app.include_router(health_check_router, tags=["HealthCheck"], prefix="/v1")
    app.include_router(orders_router, tags=["Orders"], prefix="/v1")
    app.include_router(users_router, tags=["Users"], prefix="/v1")


logging.info("Application starting...")

app = FastAPI()
inject_routers(app)

logging.info("Application started")
