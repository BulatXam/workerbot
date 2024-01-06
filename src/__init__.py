""" Импорт необходимых данных приложений для сборки бота """

from typing import List
from loguru import logger

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from src.main.router import router as main_router
from src.user.router import router as user_router
from src.worker.router import router as worker_router
from src.admin.router import router as admin_router


models: List[str] = ["src.user.models", "src.worker.models"]
bot_routers: List[Router] = [
    main_router, user_router, worker_router, admin_router
]

bot_base_router = Router(name="base_router")


@bot_base_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('На данный момент нет никакого state!')
        return

    await state.clear()
    await message.reply('Вы отменили state!')


for router in bot_routers:
    logger.info(f"Include router: {router}")
    bot_base_router.include_router(router)
