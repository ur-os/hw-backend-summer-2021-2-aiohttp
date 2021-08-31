from asyncio import Task
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        # TODO: добавить asyncio Task на запуск poll
        self.poll_task = Task(self.poll())

    async def stop(self):
        self.poll_task.cancel()
        # TODO: gracefully завершить Poller

    async def poll(self):
        await self.store.vk_api.poll()
