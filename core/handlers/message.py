from aiogram import F, Router
from aiogram.types import Message

from core.settings import settings
from core.keyboards.inlinekeyboards import response_on_message, response_on_content
from core.database import sqlite
from core.utils.time_schedule_manager import time_scheduler
from core.keyboards.admin_reply_keyboard import admin_reply_keyboard

import uuid

router = Router()


@router.message(F.from_user.id != settings.bots.admin_id, F.video | F.photo)
async def send_content_to_admin(message: Message):
    tg_id = message.from_user.id
    if not sqlite.check_user(tg_id)[0][0]:
        sqlite.create_user(message)
    if sqlite.get_ban_status(tg_id)[0][0]:
        await message.answer('К сожалению вы не можете отправлять сообщение по причине:'
                             ' Админ забанил вас к ебене матере, а еще он не написал функцию разбана'
                             'так что пишите в комменты, чтобы он вручную отредактировал БД')
    else:
        info = sqlite.get_statistic(tg_id)[0]
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
        if message.photo:
            short_id = str(uuid.uuid4())
            sqlite.create_table_short_id()
            sqlite.create_short_id(short_id, message.photo[-1].file_id, 'photo')
            await message.bot.send_photo(
                chat_id=settings.bots.admin_id,
                photo = message.photo[-1].file_id,
                reply_markup=response_on_content(message, short_id)
            )
        else:
            short_id = str(uuid.uuid4())
            sqlite.create_table_short_id()
            sqlite.create_short_id(short_id, message.video.file_id, 'video')
            await message.bot.send_video(
                chat_id=settings.bots.admin_id,
                video=message.video.file_id,
                reply_markup=response_on_content(message, short_id)
            )


@router.message(F.from_user.id != settings.bots.admin_id)
async def send_to_admin(message:Message):
    tg_id = message.from_user.id
    if not sqlite.check_user(tg_id)[0][0]:
        sqlite.create_user(message)
    if sqlite.get_ban_status(tg_id)[0][0]:
        await message.answer('К сожалению вы не можете отправлять сообщение по причине:'
                             ' Админ забанил вас к ебене матере, а еще он не написал функцию разбана'
                             'так что пишите в комменты, чтобы он вручную отредактировал БД')
    else:
        sqlite.increase_message_counter(tg_id)
        info = sqlite.get_statistic(tg_id)[0]
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


@router.message(F.from_user.id == settings.bots.admin_id, F.video | F.photo)
async def admin_post_content(message: Message):
    sqlite.create_table_sheduler()
    if message.photo:
        post_id = message.photo[-1].file_id
        send_time = time_scheduler()
        content_type = 'photo'
    else:
        post_id = message.video.file_id
        send_time = time_scheduler()
        content_type = 'video'
    try:
        sqlite.add_post_to_sheduler(post_id, send_time, content_type[0][0])
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем добавлен в отложку на время {send_time}'
        )
    except:
        await message.bot.send_message(
            chat_id=settings.bots.admin_id,
            text='Мем не смог отправиться в предложку'
        )

@router.message(F.from_user.id == settings.bots.admin_id)
async def admin_keyboard(message: Message):
    await message.bot.send_message(
        chat_id=settings.bots.admin_id,
        text='keyboard',
        reply_markup=admin_reply_keyboard
    )
