import json
import typing

from aiohttp_session import get_session, new_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


class AuthRequiredMixin:
    # TODO: можно использовать эту mixin-заготовку для реализации проверки авторизации во View
    pass