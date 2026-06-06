from fastapi import FastAPI, Request
from starlette import status
from contextlib import asynccontextmanager

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.exceptions import CustomHttpException, CustomValueError
from src.api import api_router
from src.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Dailies API")
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({
            "message": exc.errors(),
            "detail": {e["loc"][1] if len(e["loc"]) > 1 else e["loc"][0]: e["msg"].replace("Value error, ", "")
                       for e in exc.errors()}
        })
    )


@app.exception_handler(CustomHttpException)
async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "detail": exc.detail},
        headers=exc.headers,
    )


@app.exception_handler(CustomValueError)
async def custom_value_exception_handler(request: Request, exc: CustomValueError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": exc.message, "detail": exc.detail}
    )
