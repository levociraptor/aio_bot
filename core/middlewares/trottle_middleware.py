from aiogram import BaseMiddleware
from aiogram.types import Message

from core.settings import settings

import time


user_last_message_time = {}


class ThrottleMiddlewares(BaseMiddleware):
    def __init__(self, limit: float):
        super().__init__()
        self.limit = limit


    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()

        if user_id == settings.bots.admin_id:
            return await handler(event, data)

        if user_id in user_last_message_time:
            last_message_time = user_last_message_time[user_id]
            elapsed_time = current_time - last_message_time

            if elapsed_time < self.limit:
                await event.answer(f'Сообщение можно отправлять только раз в {self.limit} секунд')
                return

        user_last_message_time[user_id] = current_time

        return await handler(event, data)