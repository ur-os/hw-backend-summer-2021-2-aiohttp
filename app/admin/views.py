import re

from aiohttp.web_response import json_response

from app.web.app import View
from app.web.middlewares import HTTP_ERROR_CODES


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        try:
            data["email"]
        except KeyError:
            return json_response(
                status=400,
                data={
                    "status": HTTP_ERROR_CODES[400],
                    "message": "Wrong email format",
                    "data": {
                        "email": ["Missing data for required field."]
                    }
                })

        email = data["email"]
        admin = await self.request.app.store.admins.get_by_email(email)
        if admin:
            return json_response(
                status=200,
                data={
                    "status": "ok",
                    "data": {
                        "id": admin.id,
                        "email": admin.email
                    }
                })
        else:
            return json_response(
                status=403,
                data={
                    "status": HTTP_ERROR_CODES[403],
                    "message": "any message",
                    "data": 403
                })

    async def get(self):
        return json_response(
            status=405,
            data={
                "status": HTTP_ERROR_CODES[405],
                "message": "any message",
                "data": 405
            })


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
