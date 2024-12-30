from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.settings import settings
from core.fsm.InlineFeedback import InlineAnswer


router = Router()


@router.callback_query(F.data.startswith('Reply:'))
async def invitation_to_reply(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(InlineAnswer.message_answer)
    await state.update_data(user_chat_id=callback_query.data[len('reply:'):])
    await callback_query.message.bot.send_message(
        chat_id=settings.bots.admin_id,
        text='Ответ на сообщение:'
    )


@router.message(InlineAnswer.message_answer)
async def reply_on_message(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.send_message(
        chat_id=data['user_chat_id'],
        text='Ответ от любимого админа:'
    )
    await message.send_copy(chat_id=data['user_chat_id'])
    await state.clear()
