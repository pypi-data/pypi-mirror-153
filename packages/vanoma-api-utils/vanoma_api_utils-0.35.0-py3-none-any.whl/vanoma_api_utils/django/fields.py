import uuid
from typing import Any
from django.db import models
from .validators import validate_number


class StringField(models.CharField):
    """
    Custom field with pre-defined max length to be used as primary key,
    for pk referencing purposes, or anywhere else a short string makes sense.
    The max length is determined based on the length of UUID. Typically
    UUID have 36 characters but we added 4 more for extra breathing room.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 40
        super().__init__(*args, **kwargs)


class PrimaryKeyField(StringField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["editable"] = False
        kwargs["primary_key"] = True
        kwargs["default"] = uuid.uuid4
        super().__init__(*args, **kwargs)


class PhoneNumberField(StringField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["validators"] = [validate_number]
        super().__init__(*args, **kwargs)
