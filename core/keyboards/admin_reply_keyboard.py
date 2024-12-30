from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.settings import settings


admin_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить время последнего поста в отложке')],
    [KeyboardButton(text='Получить количество постов в отложке')],
    [KeyboardButton(text='Получить всех забанненых юзеров')],
], resize_keyboard=True)
