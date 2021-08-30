import re
import time

from aiohttp.web_response import json_response
from aiohttp_session import get_session, new_session

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
            session = await new_session(self.request)  # new shit
            session['last_visit'] = time.time()  #

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


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
