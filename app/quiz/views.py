from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized

from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
)
from app.web.app import View, Request
from app.web.utils import json_response, check_auth, error_json_response

from aiohttp_session import get_session, new_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def check_authorise(request: Request) -> bool:
    session = await get_session(request=request)
    if session:
        return True
    return False


class ThemeAddView(View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    async def post(self):
        if await check_authorise(self.request):
            title = (await self.request.json())[
                "title"
            ]  # TODO: заменить на self.data["title"] после внедрения валидации

            # TODO: проверять, что не существует темы с таким же именем, отдавать 409 если существует
            themes = await self.request.app.store.quizzes.list_themes()

            if title not in themes:
                theme = await self.store.quizzes.create_theme(title=title)
                return json_response(data=ThemeSchema().dump(theme))
            else:
                # TODO: get status from middlewares
                return error_json_response(http_status=409, status="409", message="409")
        return error_json_response(http_status=401, status="unauthorized", message="Authorise please")


class ThemeListView(View):
    async def get(self):
        if await check_authorise(self.request):
            themes = await self.request.app.store.quizzes.list_themes()
            return json_response(data={"themes": [ThemeSchema().dump(theme) for theme in themes]})  # TODO: release with scheme

        return error_json_response(http_status=401, status="unauthorized", message="Authorise please")


class QuestionAddView(View):
    async def post(self):
        if await check_authorise(self.request):
            pass
        return error_json_response(http_status=401, status="unauthorized", message="Authorise please")


class QuestionListView(View):
    async def get(self):
        if await check_authorise(self.request):
            pass
        return error_json_response(http_status=401, status="unauthorized", message="Authorise please")
