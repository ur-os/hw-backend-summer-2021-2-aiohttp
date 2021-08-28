import base64
import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        # TODO: создать админа по данным в config.yml здесь
        self.app = app
        # try:
        #     self.app.database["admins"]
        # except KeyError:
        #     self.app.database["admins"] = []
        await self.create_admin(
            self.app.config.admin.email,
            base64.b64encode(str.encode(self.app.config.admin.password)).decode()
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        admins = self.app.database.admins
        for admin in admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        # here is no checking for duplicates
        admin = Admin(
                id=self.app.database.next_admin_id,
                email=email,
                password=password
        )
        self.app.database.admins.append(admin)  # self.app.database['admins']

        return admin
