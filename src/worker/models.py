from tortoise import fields

from ..core.orm.models import AbstractBaseModel
from ..core.orm.mixins import TimestampMixin


class Review(AbstractBaseModel, TimestampMixin):
    author = fields.ForeignKeyField("models.User")

    screen_file_id = fields.CharField(max_length=1000)
    link = fields.CharField(max_length=1000)
    payment_details = fields.CharField(max_length=1000)

    status_choices = (
        ("отклонено", "отклонено"),
        ("одобрено", "одобрено"),
        ("не рассмотрено", "не рассмотрено"),
    )

    status = fields.CharField(
        choices=status_choices, default="не рассмотрено", max_length=32
    )

    unsuccess_text = fields.TextField(null=True)
