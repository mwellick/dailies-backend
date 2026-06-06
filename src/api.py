from typing import Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy import text

from fastapi.responses import JSONResponse
from src.database import get_db_session
from src.exceptions import CustomHttpException

from sqlalchemy.ext.asyncio import AsyncSession


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
async def db_health_check(db_session: AsyncSession = Depends(get_db_session)):
    try:
        await db_session.execute(text("SELECT 1"))
        return {"message": "OK"}
    except Exception:
        raise CustomHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
