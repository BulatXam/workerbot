from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.core.config import bot

from ..main.callback_factory import (
    ActionCallback, 
    ObjectCallback, 
    PaginatorCallback
)
from ..user.models import User
from ..admin import keyboards as admin_keyboards

from .models import Review
from . import states
from . import services
from . import keyboards

router = Router(name='worker')


@router.message(F.text == "Напомнить об отзыве")
async def worker_review(message: Message, state: FSMContext):
    await message.answer("Введите скрин отзыва: ")

    await state.set_state(states.WorkerReviewState.screen)


@router.message(states.WorkerReviewState.screen, F.photo)
async def worker_review(message: Message, state: FSMContext):
    await state.update_data(
        screen_file_id=message.photo[0].file_id
    )

    await message.answer("Введите ссылку, где был оставлен отзыв: ")

    await state.set_state(states.WorkerReviewState.review_link)


@router.message(states.WorkerReviewState.screen, F.text)
async def worker_review(message: Message):
    await message.answer("Вы должны ввести фото, а не текст! Не пытайтесь меня обмануть!")


@router.message(states.WorkerReviewState.review_link)
async def worker_review(message: Message, state: FSMContext):
    if "https://" not in message.text and "http://" not in message.text:
        await message.answer("Ваша ссылка должна быть вида: https://домен/ссылка/на/нужный/отзыв! Введите ссылку заново: ")

        return

    await state.update_data(
        review_link=message.text
    )

    await message.answer("Введите ваши реквизиты для выплаты вам: ")

    await state.set_state(states.WorkerReviewState.payment_details)


@router.message(states.WorkerReviewState.payment_details)
async def worker_review(message: Message, state: FSMContext):
    data = await state.get_data()
    screen_file_id = data["screen_file_id"]
    review_link = data["review_link"]
    payment_details = message.text

    worker = await User.get(user_id=message.from_user.id)

    await services.worker_send_review(
        worker=worker,
        screen_file_id=screen_file_id,
        review_link=review_link,
        payment_details=payment_details,
    )

    await message.answer("Поздравляем! Вы сделали отзыв.")

    await state.clear()


@router.callback_query(
    ObjectCallback.filter(F.action == "delete_review")
)
async def delete_review(
    call: CallbackQuery, callback_data: ObjectCallback
):
    review_id = callback_data.object_id
    review = await Review.get(id=review_id)
    review_author = await review.author
    user = await User.get(
        user_id=call.from_user.id
    )
    if review_author == user:
        await review.delete()
        await call.message.answer("Отзыв удален!")


@router.callback_query(
    ObjectCallback.filter(F.action == "get_review")
)
async def get_review(
    call: CallbackQuery, callback_data: ObjectCallback
):
    review_id = callback_data.object_id
    review = await Review.get(id=review_id)
    user = await User.get(
        user_id=call.from_user.id
    )

    if review.status == "не рассмотрено":
        reply_markup = admin_keyboards.admin_active_review_keyboard(
            user=user,
            review=review,
        )
    else:
        reply_markup = None

    await call.message.delete()

    await call.message.answer_photo(
        caption=f"Ссылка: {review.link}\n\nРеквизиты: {review.payment_details}",
        photo=review.screen_file_id,
        reply_markup=reply_markup,
    )


@router.message(F.text == "Моя история выплат")
async def payments_history(message: Message, state: FSMContext):
    review_status = "одобрено"
    await state.update_data(
        review_status=review_status
    )

    queryset = Review.filter(status=review_status)

    await message.answer(
        text="Моя история выплат",
        reply_markup=await keyboards.get_history_reviews(queryset=queryset)
    )


@router.message(F.text == "Мои активные выплаты")
async def payments_history(message: Message, state: FSMContext):
    review_status = "не рассмотрено"
    await state.update_data(
        review_status=review_status
    )

    user = await User.get(user_id=message.from_user.id)
    queryset = Review.filter(status=review_status, author=user)

    await message.answer(
        text="Мои активные выплаты",
        reply_markup=await keyboards.get_history_reviews(queryset=queryset)
    )


@router.callback_query(
    PaginatorCallback.filter(F.action == "review_paginate")
)
async def review_paginate(
    call: CallbackQuery, callback_data: PaginatorCallback, state: FSMContext
):
    state_data = await state.get_data()
    review_status = state_data["review_status"]

    user = await User.get(user_id=call.from_user.id)
    queryset = Review.filter(status=review_status, author=user)
    page = callback_data.page

    if review_status == "одобрено":
        text = "Моя история выплат"
    elif review_status == "не рассмотрено":
        text = "Мои активные выплаты"

    await call.message.answer(
        text=text,
        reply_markup=await keyboards.get_history_reviews(
            queryset=queryset,
            page_num=page
        )
    )
