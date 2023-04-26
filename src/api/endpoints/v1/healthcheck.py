from fastapi import APIRouter
from fastapi.responses import JSONResponse

health_check_router = APIRouter()


@health_check_router.get("/healthcheck")
async def health_check():
    return JSONResponse({"status": "Healthy"})
