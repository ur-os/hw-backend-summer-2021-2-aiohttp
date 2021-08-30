import json
import typing

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPUnauthorized, HTTPForbidden
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_middlewares import middleware
from aiohttp.web_response import json_response
from aiohttp_apispec import validation_middleware

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPMethodNotAllowed as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message=str(e),
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=str(e),
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message=str(e),
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(e)
        )




    # # TODO: обработать все исключения-наследники HTTPException и отдельно Exception, как server error
    #  использовать текст из HTTP_ERROR_CODES


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)

