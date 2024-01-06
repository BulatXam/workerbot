from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..worker.callback_factory import ReviewCallback
from ..worker.models import Review

from ..user.models import User

from ..main.callback_factory import ActionCallback, ObjectCallback, PaginatorCallback

from .filters import AdminFilter
from . import states
from . import services
from . import keyboards

router = Router(name="admin")
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.callback_query(
    ReviewCallback.filter(F.action == "admin_review_not_success")
)
async def admin_review_not_success(
    call: CallbackQuery, callback_data: ReviewCallback, state: FSMContext
):
    await call.message.answer("Введите причину отказа: ")
    await state.update_data(
        review_id=callback_data.review_id
    )
    await state.set_state(states.ReviewNotSuccessState.text)


@router.message(states.ReviewNotSuccessState.text)
async def admin_review_not_success_text(message: Message, state: FSMContext):
    text = message.text

    state_data = await state.get_data()
    review_id = state_data['review_id']

    review = await Review.get(id=review_id)
    user = await User.get(user_id=message.from_user.id)

    await services.review_not_success(user=user, review=review, text=text)

    await state.clear()


@router.callback_query(
    ReviewCallback.filter(F.action == "admin_review_success")
)
async def admin_review_success(
    call: CallbackQuery, callback_data: ReviewCallback
):
    review_id=callback_data.review_id

    review = await Review.get(id=review_id)
    user = await User.get(user_id=call.from_user.id)

    await services.review_success(user=user, review=review)


@router.message(F.text == "Закрытые отзывы")
async def payments_history(message: Message, state: FSMContext):
    review_status = "одобрено"
    await state.update_data(
        review_status=review_status
    )

    queryset = Review.filter(status=review_status)

    await message.answer(
        text="Закрытые отзывы",
        reply_markup=await keyboards.get_history_reviews(
            queryset=queryset
        )
    )


@router.message(F.text == "Активные выплаты")
async def payments_history(message: Message, state: FSMContext):
    review_status = "не рассмотрено"
    await state.update_data(
        review_status=review_status
    )

    queryset = Review.filter(status=review_status)

    await message.answer(
        text="Активные выплаты",
        reply_markup=await keyboards.get_history_reviews(
            queryset=queryset
        )
    )


@router.callback_query(
    PaginatorCallback.filter(F.action == "admin_review_paginate")
)
async def review_paginate(
    call: CallbackQuery, callback_data: PaginatorCallback, state: FSMContext
):
    state_data = await state.get_data()
    try:
        review_status = state_data["review_status"]
    except KeyError:
        review_status = ""

    print(review_status)
    print(callback_data.page)

    queryset = Review.filter(status=review_status)
    page = callback_data.page

    if review_status == "одобрено":
        text = "Закрытые выплаты"
    elif review_status == "не рассмотрено":
        text = "Активные выплаты"
    else:
        text = "Отзывов больше нет!"

    await call.message.answer(
        text=text,
        reply_markup=await keyboards.get_history_reviews(
            queryset=queryset,
            page_num=page
        )
    )
