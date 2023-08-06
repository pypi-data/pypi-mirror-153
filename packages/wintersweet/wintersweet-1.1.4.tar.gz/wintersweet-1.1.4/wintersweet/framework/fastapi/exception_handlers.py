from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from wintersweet.framework.fastapi.response import Response, HTTP400Response, HTTPExceptionResponse
from wintersweet.utils.base import Utils


async def http_exception_handler(
        request: Request, exc: HTTPException
) -> Response:

    headers = getattr(exc, 'headers', None)
    if headers:
        return HTTPExceptionResponse(status_code=exc.status_code, detail=exc.detail, headers=exc.headers)
    else:
        return HTTPExceptionResponse(status_code=exc.status_code, detail=exc.detail)


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> Response:
    Utils.log.error(f'{exc.body} --> {[err.get("loc") for err in exc.errors()]}')

    return HTTP400Response(content=jsonable_encoder(exc.errors()))
