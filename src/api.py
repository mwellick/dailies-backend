from typing import Any
from pydantic import BaseModel
from fastapi import APIRouter
from starlette import status
from sqlalchemy import text

from fastapi.responses import JSONResponse
from src.exceptions import CustomHttpException
from src.database import sessionmanager


class ErrorResponse(BaseModel):
    message: str
    detail: Any


class ValidationErrorResponse(ErrorResponse):
    detail: dict[str, str] | None


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ErrorResponse},
    }
)


@api_router.get("/db-health-check", status_code=status.HTTP_200_OK)
async def db_health_check():
    try:
        async with sessionmanager.connect() as connection:
            await connection.execute(text("SELECT 1"))
            return {"message": "OK"}
    except Exception:
        raise CustomHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
