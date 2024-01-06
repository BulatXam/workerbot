from ..core.config import bot

from ..worker.models import Review
from ..user.models import User


async def review_success(user: User, review: Review):
    review.status = "одобрено"
    await review.save()

    review_author = await review.author

    await bot.send_message(
        chat_id=review_author.user_id,
        text=f"Поздрвавляю, ваш отзыв одобрен админом {user.username}!"
    )

    for admin in await User.filter(is_worker=False):
        await bot.send_message(
            chat_id=admin.user_id,
            text=f"Отзыв @{review_author.username} одобрен админом {user.username}!"
        )


async def review_not_success(user: User, review: Review, text: str):
    review.unsuccess_text = text
    review.status = "отклонено"
    await review.save()

    review_author = await review.author

    await bot.send_message(
        chat_id=review_author.user_id,
        text=f"Ваш отзыв был отклонен админом {user.username}!\n\nПричина:\n"+text
    )

    for admin in await User.filter(is_worker=False):
        await bot.send_message(
            chat_id=admin.user_id,
            text=f"Отзыв @{review_author.username} был отклонен админом {user.username}!"
        )
