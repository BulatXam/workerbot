from aiogram.fsm.state import StatesGroup, State


class WorkerReviewState(StatesGroup):
    screen = State()
    review_link = State()
    payment_details = State()
