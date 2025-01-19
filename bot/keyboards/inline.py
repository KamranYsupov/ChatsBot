from typing import Dict, Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from django.conf import settings


def get_inline_keyboard(*, buttons: Dict[str, str], sizes: Tuple = (1, 2)):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_inline_menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='Список групп 🗂',
            callback_data='chats_1'
        )
    )
    
    keyboard.add(
        InlineKeyboardButton(
            text='FAQ ❓',
            callback_data='faq'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Связатся с администратором ☎️',
            url=settings.ADMIN_ACCOUNT_LINK,
        )
    )
    
    return keyboard.adjust(1, 1, 1).as_markup()


inline_cancel_keyboard = get_inline_keyboard(
    buttons={'Отмена ❌': 'cancel'}
)
