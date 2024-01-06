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
            action="review_paginate",
            page=page.next_page_number(),
        ).pack(), 
    )


async def back_button_review(page: Page):
    return InlineKeyboardButton(
        text=f"{page}", callback_data=PaginatorCallback(
            action="review_paginate",
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
                action="c",
            ).pack()
        ),
        page_num=page_num
    )
