from aiogram import Bot, Dispatcher

from core.settings import settings
from core.utils.commands import set_commands
from core.handlers.message import router as message_router
from core.handlers.commands import router as command_router
from core.handlers.fsm_answer import router as fsm_router
from core.handlers.callback_query import router as callback_router
from core.handlers.admin_reply_message import router as admin_keyboard_router
from core.database import queries, start_table
from core.middlewares.trottle_middleware import ThrottleMiddlewares
from core.keyboards.admin_reply_keyboard import admin_reply_keyboard

from datetime import datetime
import asyncio


async def start_bot(bot: Bot):
    await set_commands(bot)
    await start_table.create_all_tables()
    await bot.send_message(settings.bots. admin_id, 'START')
    await bot.send_message(
        chat_id=settings.bots.admin_id,
        text="keyboard",
        reply_markup=admin_reply_keyboard
    )


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'STOP')


async def schedule_post(bot: Bot):
    while True:
        time = datetime.now()
        posts = await queries.get_posts(time)
        print(posts)
        for post in posts:
            post_id, file_id, content_type, author = post
            try:
                if content_type == 'photo':
                    if author == "user":
                        await bot.send_photo(chat_id=settings.bots.channel_link, photo=file_id, caption="#мем_из_предложки")
                    else:
                        await bot.send_photo(chat_id=settings.bots.channel_link, photo=file_id)
                elif content_type == 'video':
                    if author == "user":
                        await bot.send_video(chat_id=settings.bots.channel_link, video=file_id, caption="#мем_из_предложки")
                    else:
                        await bot.send_video(chat_id=settings.bots.channel_link, video=file_id)
                queries.delete_sent_post(post_id)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(60)


async def start():
    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher()
    dp.message.middleware(ThrottleMiddlewares(limit=10))
    dp.include_routers(
        fsm_router,
        admin_keyboard_router,
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
