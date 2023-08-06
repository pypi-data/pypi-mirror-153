import asyncio
from random import random


class AsyncioSafeTasks():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tasks = {}

    def create_task(self, awaitable):
        id = random()
        self._tasks[id] = asyncio.create_task(self._do_task(id, awaitable))

    async def _do_task(self, id, awaitable):
        v = await awaitable
        del self._tasks[id]
        return v

    def cleanup_tasks(self):
        for task in self._tasks.values():
            try:
                task.cancel()
            except Exception as e:
                pass
        self._tasks = {}
