from aiogram import F, Router
from aiogram.types import CallbackQuery

from core.settings import settings
from core.database import queries
from core.utils.time_schedule_manager import time_scheduler

from datetime import datetime, timedelta

router = Router()


@router.callback_query(F.data.startswith("Approve:"))
async def post_content(callback_query: CallbackQuery):
    separator = callback_query.data.index('_')
    tg_id = int(callback_query.data[len('Approve:'):separator])
    await queries.increase_approved_message_counter(tg_id)

    short_id = callback_query.data[separator+1:]
    post_id = await queries.get_file_id(short_id)
    post_id = post_id[0][0]
    content_type = await queries.get_content_type(short_id)
    send_time = time_scheduler()
    try:
        await queries.add_post_to_sheduler(post_id, send_time, content_type[0][0])
        await callback_query.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем добавлен в отложку на время {send_time}'
        )
        await callback_query.bot.send_message(
            chat_id=tg_id,
            text="""Ваш мем был добавлен в отложку канала,
                 админ это не забудет, не серьезно не забудет
                 у него теперь есть база данных с вашей инфой"""
        )
    except Exception as e:
        await callback_query.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем не смог отправиться в предложку по причине {e}'
        )


@router.callback_query(F.data.startswith("Reject:"))
async def reject_user(callback_query: CallbackQuery):
    tg_id = int(callback_query.data[len("Reject:"):])
    await queries.increase_rejected_message_counter(tg_id)
    await callback_query.message.bot.send_message(
        chat_id=tg_id,
        text='Сорямба, ваш мем отклонен'
    )


@router.callback_query(F.data.startswith("Ban:"))
async def ban_user(callback_query: CallbackQuery):
    tg_id = int(callback_query.data[len('Ban:'):-2])
    ban_duration = callback_query.data[-1]
    if ban_duration == "1":
        time_to_unban = datetime.now() + timedelta(hours=1)
    elif ban_duration == "2":
        time_to_unban = datetime.now() + timedelta(hours=6)
    elif ban_duration == "3":
        time_to_unban = datetime.now() + timedelta(days=1)
    elif ban_duration == "4":
        time_to_unban = datetime.now() + timedelta(days=3)
    await queries.set_ban(tg_id, time_to_unban)
    await callback_query.message.bot.send_message(
        chat_id=settings.bots.admin_id,
        text='Пользователь попал в бан'
    )
