from tortoise import fields

from ..core.orm.models import AbstractBaseModel
from ..core.orm.mixins import TimestampMixin


class User(AbstractBaseModel, TimestampMixin):
    user_id = fields.BigIntField(unique=True)
    username = fields.TextField(null=True)
    first_name = fields.TextField()
    last_name = fields.TextField(null=True)
    is_worker = fields.BooleanField(default=True)
