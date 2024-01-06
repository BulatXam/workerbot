from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.core.settings import settings

from ..user.models import User

from .keyboards import get_start_keyboard


router = Router(name="main")


@router.message(
    Command("start"), F.chat.type == 'private'
)
async def profile(message: Message):
    user = await User.get_or_create(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
        is_worker=False if message.from_user.id in settings.OWNER_IDS else True
    )
    print(True if message.from_user.id in settings.OWNER_IDS else False)
    await message.answer(
        "Добро пожаловать в бота!",
        reply_markup=get_start_keyboard(user=user[0])
    )
