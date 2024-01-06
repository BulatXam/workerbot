from aiogram.utils.keyboard import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    KeyboardButton, 
    ReplyKeyboardMarkup,
)

from ..main.callback_factory import PaginatorCallback

from ..worker.callback_factory import ReviewCallback
from ..worker.models import Review

from ..user.models import User


def admin_active_review_keyboard(user: User, review: Review) -> ReplyKeyboardMarkup:
    if review.status == "не рассмотрено":
        if not user.is_worker:
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отказаться",
                        callback_data=ReviewCallback(
                            action="admin_review_not_success",
                            review_id=review.id,
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text="Перевел",
                        callback_data=ReviewCallback(
                            action="admin_review_success",
                            review_id=review.id,
                        ).pack()
                    )
                ]
            ]
            paginator_callback_action = "admin_review_paginate"
        else:
            paginator_callback_action = "review_paginate"
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        text="Отмена",
                        callback_data=ObjectCallback(
                            action="delete_review",
                            object_id=review.id,
                        ).pack()
                    ),
                ]
            ]
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            *inline_keyboard,
            [InlineKeyboardButton(
                text="Назад",
                callback_data=PaginatorCallback(action=paginator_callback_action).pack()
            )]
        ]
    )


from tortoise.queryset import QuerySet

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..core.utils.paginator import get_paginate_keyboard, Page

from ..main.callback_factory import ObjectCallback, ActionCallback, PaginatorCallback

from ..worker.models import Review    


async def i_review(i: Review):
    return InlineKeyboardButton(
        text=i.link,
        callback_data=ObjectCallback(
            action="get_review",
            object_id=i.id,
        ).pack(),
    )


async def next_button_review(page: Page):
    return InlineKeyboardButton(
        text=f"{page}", callback_data=PaginatorCallback(
            action="admin_review_paginate",
            page=page.next_page_number(),
        ).pack(), 
    )


async def back_button_review(page: Page):
    return InlineKeyboardButton(
        text=f"{page}", callback_data=PaginatorCallback(
            action="admin_review_paginate",
            page=page.previous_page_number(),
        ).pack(), 
    )


async def get_history_reviews(queryset: QuerySet, page_num: int = 1):
    return await get_paginate_keyboard(
        queryset=queryset,
        i_button=i_review,
        next_button=next_button_review,
        back_button=back_button_review,
        none_button=InlineKeyboardButton(
            text="Назад",
            callback_data=ActionCallback(
                action="w",
            ).pack()
        ),
        page_num=page_num
    )

