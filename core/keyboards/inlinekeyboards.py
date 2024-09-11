from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def response_on_message(message):
    response_on_message_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Ответить на сообщение', callback_data=f'Reply:{message.chat.id}'),
            InlineKeyboardButton(text='В бан',  callback_data=f'Ban:{message.from_user.id}')]
    ])
    return response_on_message_keyboard

def response_on_content(message, content=""):
    response_on_content_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Запостить мем', callback_data=f'Approve:{message.from_user.id}_{content}'),
            InlineKeyboardButton(text='В бан', callback_data=f'Ban:{message.from_user.id}')],
             [InlineKeyboardButton(text='Отклонить', callback_data=f'Reject:{message.from_user.id}')]
    ])
    return response_on_content_keyboard