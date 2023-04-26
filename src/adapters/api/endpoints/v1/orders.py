import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.entities.orders.schemas import CreateOrderSchema
from src.entities.orders.services import OrderService
from src.shared.auth_bearer_validator import AuthBearerValidator

orders_router = APIRouter()


@orders_router.get("/orders/get_all_orders")
async def get_all_orders(token_infos: dict = Depends(AuthBearerValidator())):
    return OrderService.get_all_orders()


@orders_router.post("/orders/create")
async def create_order(
    order: CreateOrderSchema, token_infos: dict = Depends(AuthBearerValidator())
):
    try:
        OrderService.create_order(order)
        return JSONResponse(
            {"message": "Compra registrada"}, status_code=status.HTTP_201_CREATED
        )
    except Exception as err:
        logging.error(err)
        return JSONResponse(
            {"message": "Erro ao processar sua compra"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
