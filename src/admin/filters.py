from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from ..core.settings import settings


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message|CallbackQuery) -> Union[bool, Dict[str, Any]]:
        if message.from_user.id in settings.OWNER_IDS:
            return True
