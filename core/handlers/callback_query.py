from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.settings import settings
from core.fsm.InlineFeedback import InlineAnswer
from core.database import sqlite
from core.utils.time_schedule_manager import time_scheduler

from datetime import datetime, time, date, timedelta

router = Router()


@router.callback_query(F.data.startswith("Approve:"))
async def post_content(callback_query: CallbackQuery):
    separator = callback_query.data.index('_')
    tg_id = int(callback_query.data[len('Approve:'):separator])
    sqlite.increase_approved_message_counter(tg_id)

    short_id = callback_query.data[separator+1:]
    post_id = sqlite.get_file_id(short_id)[0][0]
    content_type = sqlite.get_content_type(short_id)
    send_time = time_scheduler()
    sqlite.create_table_sheduler()
    try:
        sqlite.add_post_to_sheduler(post_id, send_time, content_type[0][0])
        await callback_query.bot.send_message(
            chat_id=settings.bots.admin_id,
            text=f'Мем добавлен в отложку на время {send_time}'
        )
        await callback_query.bot.send_message(
            chat_id=tg_id,
            text=F'Ваш мем был добавлен в отложку канала, '
                 F'админ это не забудет, не серьезно не забудет у него теперь есть база данных с вашей инфой'
        )
    except:
        await callback_query.bot.send_message(
            chat_id=settings.bots.admin_id,
            text='Мем не смог отправиться в предложку'
        )


@router.callback_query(F.data.startswith("Reject:"))
async def reject_user(callback_query: CallbackQuery):
    tg_id = int(callback_query.data[len("Reject:"):])
    sqlite.increase_rejected_message_counter(tg_id)
    await callback_query.message.bot.send_message(
        chat_id=tg_id,
        text=f'Сорямба, ваш мем отклонен'
    )


@router.callback_query(F.data.startswith("Ban:"))
async def ban_user(callback_query: CallbackQuery):
    tg_id = int(callback_query.data[len('Ban:'):])
    sqlite.set_ban(tg_id)
    await callback_query.message.bot.send_message(
        chat_id=settings.bots.admin_id,
        text='Пользователь попал в бан'
    )