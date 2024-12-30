from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from core.database import queries

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    user_exists = await queries.check_user(message.from_user.id)
    if not user_exists[0][0]:
        await queries.create_user(message)
    await message.answer(
        text=f"{markdown.hide_link('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQl1lzjthqrJYdbukbAvqUM0z5UdeamyyZJbQ&s')}Hello!",
        parse_mode=ParseMode.HTML
    )


@router.message(Command('help'))
async def get_help(message: Message):
    text = ('Бот обратной связи.\n'
            'Пишите сообщения, отправляйте картинки и видосы, все это придет админу и он сможет на это ответить.'
            'Но аккуратно, функция бана тоже присутсвует')
    await message.answer(text=text)
