import asyncio
import typing
from typing import Optional

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject, UpdateMessage
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        # TODO: добавить создание aiohttp ClientSession,
        self.session = ClientSession()
        await self._get_long_poll_service()
        poll = Poller(store=app.store)
        await poll.start()
        #  получить данные о long poll сервере с помощью метода groups.getLongPollServer
        #  вызвать метод start у Poller

    async def disconnect(self, app: "Application"):
        if self.session is not None:
            await self.session.close()
        if self.poller is not None:
            await self.poller.stop()
        # TODO: закрыть сессию и завершить поллер

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        async with self.session.get(
                'https://api.vk.com/method/groups.getLongPollServer?'
                'group_id={group_id}&'
                'access_token={access_token}&'
                'v={v}'.format(
                    group_id="206827067",
                    access_token="196378a02c47fb84ea4c27a29d0cbe312bf4cd8192d89d9c502446e008de4794d97e3a184fec0ea01532e",
                    v="5.50"
                )
        ) as resp:
            resp_json = (await resp.json())["response"]
            self.key = resp_json["key"]
            self.server = resp_json["server"]
            self.ts = resp_json["ts"]

    async def poll(self):
        async with self.session.get(
                '{server}?'
                'act=a_check&'
                'key={key}&'
                'key={key}&'
                'ts={ts}'
                'wait={wait}'.format(
                    server=self.server,
                    key=self.key,
                    ts=int(self.ts),
                    wait="25"
                )
        ) as resp:
            resp_json = (await resp.json())["response"]
            self.ts = resp_json["ts"]

            updates = list[Update]
            for update in resp_json["updates"]:
                if update["type"] == "message_new":
                    updates.append(
                        Update(
                            type="message_new",
                            object=UpdateObject(
                                UpdateMessage(
                                    id=update["object"]["id"],
                                    from_id=update["object"]["176500961"],
                                    text=update["object"]["body"]
                                )
                            )
                        )
                    )
            self.app.store.bots_manager.handle_updates(updates)

    async def send_message(self, message: Message) -> None:
        async with self.session.get(
                'https://api.vk.com/method/messages.send?'
                'peer_id={peer_id}&'
                'message={message}&'
                'user_id={user_id}'
                'access_token={access_token}&'
                'v={v}'.format(
                    peer_id="206827067",
                    message=message.text,
                    user_id=message.user_id,
                    access_token="196378a02c47fb84ea4c27a29d0cbe312bf4cd8192d89d9c502446e008de4794d97e3a184fec0ea01532e",
                    v="5.50"
                )
        ) as resp:
            print(resp.json())
