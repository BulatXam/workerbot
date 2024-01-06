from aiogram.fsm.state import StatesGroup, State


class ReviewNotSuccessState(StatesGroup):
    text = State()
