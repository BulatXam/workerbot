from aiogram.filters.callback_data import CallbackData


class ActionCallback(CallbackData, prefix="action"):
    action: str

class ObjectCallback(CallbackData, prefix="object"):
    action: str
    object_id: int


class PaginatorCallback(CallbackData, prefix="paginator"):
    action: str
    page: int = 1
