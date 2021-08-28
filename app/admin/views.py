import re

from aiohttp.web_response import json_response

from app.web.app import View


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()

        if re.search(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', data["email"]) is None:
            return json_response(status=400, data={
                "status": "bad_request",
                "message": "Wrong email format",
                "data": 400
            })

        email = data["email"]
        admin = await self.request.app.store.admins.get_by_email(email)
        if admin:
            return json_response(status=200, data={
                "status": "ok",
                "data": {
                    "id": admin.id,
                    "email": admin.email
                }
            })
        else:
            return json_response(status=400, data={
                "status": "bad_request",
                "message": "any message",
                "data": 403
            })


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
