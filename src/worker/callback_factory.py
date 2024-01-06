from aiogram.filters.callback_data import CallbackData


class ReviewCallback(CallbackData, prefix="action"):
    action: str
    review_id: int
