from aiogram.types import Message
from aiogram import F, Router

from core.settings import settings
from core.database import sqlite

router = Router()


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить время последнего поста в отложке')
async def get_time_last_schedule_message(message: Message):
    last_time_post = str(sqlite.get_time_last_post()[0][0])
    await message.answer(last_time_post)


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить количество постов в отложке')
async def get_posts_quantity(message: Message):
    quantity_posts = str(sqlite.get_posts_quantity()[0][0])
    await message.answer(quantity_posts)


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить всех забанненых юзеров')
async def get_posts_quantity(message: Message):
    ban_users = sqlite.get_ban_users()
    for user in ban_users:
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f"Пользователь: {user[2]} \n"
                 f"C ID: {user[1]}"
        )