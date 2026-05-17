from typing import Any
from pydantic import BaseModel
from fastapi import APIRouter

from fastapi.responses import JSONResponse

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


@api_router.get("/")
async def main():
    return "Hello world"
