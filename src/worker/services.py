from ..core.config import bot

from ..user.models import User

from ..admin import keyboards as admin_keyboards

from . import keyboards
from .models import Review


async def worker_send_review(
    worker: User, screen_file_id: int, review_link: str, payment_details: str
):
    review = await Review.create(
        author=worker,
        screen_file_id=screen_file_id,
        link=review_link,
        payment_details=payment_details
    )

    for admin in await User.filter(is_worker=False):
        await bot.send_photo(
            chat_id=admin.user_id,
            photo=screen_file_id,
            caption=\
            f"Ссылка на отзыв: <code>{review_link}</code> \n\n"
            f"Реквизиты: <code>{payment_details}</code>",
            parse_mode="HTML",
            reply_markup=admin_keyboards.admin_active_review_keyboard(
                user=admin,
                review=review
            )
        )
