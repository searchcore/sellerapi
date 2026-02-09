from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import setup_dishka
import logging

from src.core.config import config
from src.core.exceptions import BaseAppException
from src.api.exceptions import APIError
from src.api.v1.router import router as v1_router

from src.infrastructure.setup import setup_infrastructure, setup_mediator


logger = logging.getLogger(__name__)


description = """
Seller API helps you buy digital goods

## Customer

As customer you can:
* Purchase products by **purchase tokens**
> Purchase token is a *unique key* with main purpose to *buy products* without user authentification.
Each purchase token has **it's own buy limit**, which **can be increased** by administration.
"""

app = FastAPI(
    title=config.PROJECT_NAME,
    description=description,
    debug=config.DEBUG,
)

container = setup_infrastructure()
mediator = setup_mediator(container)
app.state.mediator = mediator


setup_dishka(container=container, app=app)


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.exception(
        "api_error_occured",
        exc_info=False,
        extra={
            "code": exc.code,
        }
    )
    return JSONResponse(
        {
            "error": {
                "code": exc.code,
                "details": exc.details,
                "params": exc.params,
            }
        },
        exc.status_code
    )


@app.exception_handler(BaseAppException)
async def api_error_handler(request: Request, exc: BaseAppException):
    logger.exception(
        "app_error_occured",
        exc_info=False,
        extra={
            "code": exc.code,
        }
    )
    return JSONResponse(
        {
            "error": {
                "code": exc.code,
                "details": exc.details,
                "params": exc.params,
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "unknown_error_occured",
        stack_info=True,
    )
    return JSONResponse({"error":"Internal server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


app.include_router(v1_router, prefix=config.API_V1_PREFIX)