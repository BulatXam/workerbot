from aiogram.utils.keyboard import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    KeyboardButton, 
    ReplyKeyboardMarkup,
)

from ..user.models import User


def get_start_keyboard(user: User) -> ReplyKeyboardMarkup:
    if user.is_worker:
        keyboard=[
            [
                KeyboardButton(text="Мои активные выплаты"),
            ],
            [
                KeyboardButton(text="Моя история выплат"),
                KeyboardButton(text="Напомнить об отзыве"),                
            ]
        ]
    else:
        keyboard=[
            [
                KeyboardButton(text="Активные выплаты"),
            ],
            [
                KeyboardButton(text="Закрытые отзывы"),                
            ]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard
    )
