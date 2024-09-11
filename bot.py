from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command

from core.settings import settings
from core.utils.commands import set_commands
from core.handlers.message import router as message_router
from core.handlers.commands import  router as command_router
from core.handlers.fsm_answer import router as fsm_router
from core.handlers.callback_query import router as callback_router
from core.handlers.admin_reply_message import router as admin_keyboard_router
from core.database import sqlite
from core.middlewares.trottle_middleware import ThrottleMiddlewares

from datetime import datetime
import asyncio
import logging


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots. admin_id, 'START')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'STOP')


async def schedule_post(bot: Bot):
    while True:
        time = datetime.now()
        posts = sqlite.get_posts(time)
        print(posts)
        for post in posts:
            post_id, file_id, content_type = post
            try:
                if content_type == 'photo':
                    await bot.send_photo(chat_id=settings.bots.channel_link, photo=file_id)
                elif content_type == 'video':
                    await bot.send_video(chat_id=settings.bots.channel_link, video=file_id)
                sqlite.delete_sent_post(post_id)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')

    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher()
    dp.message.middleware(ThrottleMiddlewares(limit=30))
    dp.include_routers(
        admin_keyboard_router,
        fsm_router,
        callback_router,
        command_router,
        message_router
    )

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    asyncio.create_task(schedule_post(bot))

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())