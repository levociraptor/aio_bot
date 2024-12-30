from aiogram import F, Router
from aiogram.types import Message

from core.settings import settings
from core.keyboards.inlinekeyboards import (response_on_message,
                                    response_on_content,
                                    )
from core.database import queries

import datetime
import uuid

router = Router()


@router.message(F.from_user.id != settings.bots.admin_id, F.video | F.photo)
async def send_content_to_admin(message: Message):
    tg_id = message.from_user.id
    user_exists = await queries.check_user(tg_id)
    if not user_exists[0][0]:
        await queries.create_user(message)
    ban_status = await queries.get_ban_status(tg_id)
    if ban_status[0][0]:
        time_to_unban = await queries.get_time_to_unban(tg_id)
        if datetime.datetime.now() >= [0][0]:
            await queries.set_unban(tg_id)
        else:
            await message.answer('К сожалению вы не можете отправлять сообщение по причине:'
                                ' Админ забанил вас к ебене матере.'
                                f' Время разбана: {time_to_unban}')
    else:
        info = await queries.get_statistic(tg_id)
        info = info[0]
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Пользователь {info[0]}, \nc ником {info[1]}\n'
                 f'Отправил вам мем\n'
                 f'Статистика пользователя: \n'
                 f'Отправленных сообщений: {info[2]}\n'
                 f'Мемов отправлено: {info[3] + info[4]}\n'
                 f'Из них одобренно: {info[3]} и отклоненно: {info[4]}\n'
                 f'Ну собсна мем: '
        )
        short_id = str(uuid.uuid4())
        if message.photo:
            await queries.create_short_id(short_id, message.photo[-1].file_id, 'photo')
            await message.bot.send_photo(
                chat_id=settings.bots.admin_id,
                photo=message.photo[-1].file_id,
                reply_markup=response_on_content(message, short_id)
            )
        else:
            await queries.create_short_id(short_id, message.video.file_id, 'video')
            await message.bot.send_video(
                chat_id=settings.bots.admin_id,
                video=message.video.file_id,
                reply_markup=response_on_content(message, short_id)
            )


@router.message(F.from_user.id != settings.bots.admin_id)
async def send_to_admin(message: Message):
    tg_id = message.from_user.id
    user_exists = await queries.check_user(tg_id)
    if not user_exists[0][0]:
        await queries.create_user(message)
    ban_status = await queries.get_ban_status(tg_id)
    if ban_status[0][0]:
        time_to_unban = await queries.get_time_to_unban(tg_id)
        print(time_to_unban)
        print(time_to_unban[0][0])
        if datetime.datetime.now() >= time_to_unban[0][0]:
            await queries.set_unban(tg_id)
        else:
            await message.answer('К сожалению вы не можете отправлять сообщение по причине:'
                                ' Админ забанил вас к ебене матере.'
                                f' Время разбана: {time_to_unban[0][0]}')
    else:
        await queries.increase_message_counter(tg_id)
        info = await queries.get_statistic(tg_id)
        info = info[0]
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Пользователь {info[0]}, \nc ником {info[1]}\n'
                 f'Отправил вам сообщение\n'
                 f'Статистика пользователя: \n'
                 f'Отправленных сообщений: {info[2]}\n'
                 f'Мемов отправлено: {info[3] + info[4]}\n'
                 f'Из них одобренно: {info[3]} и отклоненно: {info[4]}\n'
                 f'Сообщение:'
        )
        await message.copy_to(
            chat_id=settings.bots.admin_id,
            reply_markup=response_on_message(message)
        )
