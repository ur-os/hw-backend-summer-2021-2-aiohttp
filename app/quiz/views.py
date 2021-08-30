from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized, HTTPBadRequest, HTTPNotFound, HTTPConflict

from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema, AnswerSchema, QuestionSchema, ListQuestionSchema,
)
from app.web.app import View, Request
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response, check_auth, error_json_response
from app.web.middlewares import HTTP_ERROR_CODES

from aiohttp_session import get_session, new_session, setup
from aiohttp_apispec import docs, request_schema, response_schema


async def check_authorise(request: Request) -> bool:
    session = await get_session(request=request)
    if session:
        return True
    return False


class ThemeAddView(View):
    @docs(tags=['quiz'], summary='Add new theme', description='Add new theme to database')
    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        if await check_authorise(self.request):
            title = self.data["title"]
            themes = await self.request.app.store.quizzes.list_themes()

            if title in [ThemeSchema().dump(theme)["title"] for theme in themes]:
                return error_json_response(http_status=409, status=HTTP_ERROR_CODES[409], message="Theme already exist")

            theme = await self.store.quizzes.create_theme(title=title)
            return json_response(data=ThemeSchema().dump(theme))

        return error_json_response(http_status=401, status=HTTP_ERROR_CODES[401], message="Authorise please")


class ThemeListView(View):
    async def get(self):
        if await check_authorise(self.request):
            themes = await self.request.app.store.quizzes.list_themes()
            return json_response(data={
                "themes": [ThemeSchema().dump(theme) for theme in themes]
            })  # TODO: release with scheme
        raise HTTPUnauthorized


class QuestionAddView(View):
    @docs(tags=['quiz'], summary='Add new question', description='Add new question to database')
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        if await check_authorise(self.request):
            theme_id = self.data["theme_id"]
            if await self.request.app.store.quizzes.get_theme_by_id(theme_id) is None:
                raise HTTPNotFound

            title = self.data["title"]
            answers = [AnswerSchema.load(AnswerSchema(), a) for a in self.data["answers"]]
            corrects = [answer["is_correct"] for answer in answers]
            questions = await self.request.app.store.quizzes.list_questions()

            if len(answers) < 2:
                raise HTTPBadRequest
            if (True not in corrects) ^ (False not in corrects):
                raise HTTPBadRequest
            if title in [QuestionSchema().dump(question)["title"] for question in questions]:
                raise HTTPConflict

            question = await self.store.quizzes.create_question(
                title=title,
                theme_id=theme_id,
                answers=answers
            )
            return json_response(data=QuestionSchema().dump(question))
        raise HTTPUnauthorized


class QuestionListView(View):
    @docs(tags=['quiz'], summary='List questions', description='List questions from database')
    @request_schema(ListQuestionSchema)
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        if await check_authorise(self.request):
            questions = await self.request.app.store.quizzes.list_questions()
            return json_response(data={"questions": [QuestionSchema().dump(question) for question in questions]})  # TODO: release with scheme
        #
        # "id": int(question.id),
        # "title": str(question.title),
        # "theme_id": int(question.theme_id),
        # "answers": [answer2dict(answer) for answer in question.answers],
        raise HTTPUnauthorized
