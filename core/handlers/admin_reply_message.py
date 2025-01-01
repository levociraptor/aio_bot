from aiogram.types import Message
from aiogram import F, Router

from core.settings import settings
from core.database import queries
from core.utils.time_schedule_manager import time_scheduler


router = Router()


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить время последнего поста в отложке')
async def get_time_last_schedule_message(message: Message):
    last_time_post = await queries.get_time_last_post()
    await message.answer(str(last_time_post[0][0]))


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить количество постов в отложке')
async def get_posts_quantity(message: Message):
    quantity_posts = await queries.get_posts_quantity()
    await message.answer(str(quantity_posts[0][0]))


@router.message(F.from_user.id == settings.bots.admin_id, F.text == 'Получить всех забанненых юзеров')
async def get_ban_users(message: Message):
    ban_users = await queries.get_ban_users()
    if ban_users:
        for user in ban_users:
            await message.bot.send_message(
                chat_id=settings.bots.admin_id,
                text=f"Пользователь: {user[2]} \n"
                    f"C ID: {user[1]}"
            )
    else:
        await message.bot.send_message(
                chat_id=settings.bots.admin_id,
                text=f"Нет забанненых пользователей")


@router.message(F.from_user.id == settings.bots.admin_id, F.text.startswith('/unban'))
async def unban_user(message: Message):
    id = message.text[len("/unban"):].strip()
    if id.isalnum():
        user_exists = await queries.check_user(int(id))
        if user_exists[0][0]:
            ban_status = await queries.get_ban_status(int(id))
            if ban_status[0][0]:
                await queries.set_unban(int(id))
                await message.bot.send_message(
                    chat_id=settings.bots.admin_id,
                    text="Юзер разбанен")
            else:
                await message.bot.send_message(
                    chat_id=settings.bots.admin_id,
                    text="Юзер не забанен")
        else:
            await message.bot.send_message(
                chat_id=settings.bots.admin_id,
                text="Юзер не был найден")
    else:
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text="Вам нужно отправить валидный id")


@router.message(F.from_user.id == settings.bots.admin_id, F.video | F.photo)
async def admin_post_content(message: Message):
    if message.photo:
        post_id = message.photo[-1].file_id
        send_time = await time_scheduler()
        content_type = 'photo'
    else:
        post_id = message.video.file_id
        send_time = await time_scheduler()
        content_type = 'video'
    try:
        author = "admin"
        await queries.add_post_to_scheduler(post_id, send_time, content_type, author)
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем добавлен в отложку на время {send_time}'
        )
    except Exception as e:
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем не смог отправиться в предложку/nИсключение: {e}'
        )
