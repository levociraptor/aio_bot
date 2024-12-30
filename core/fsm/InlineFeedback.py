from aiogram.fsm.state import StatesGroup, State


class InlineAnswer(StatesGroup):
    message_answer = State()
