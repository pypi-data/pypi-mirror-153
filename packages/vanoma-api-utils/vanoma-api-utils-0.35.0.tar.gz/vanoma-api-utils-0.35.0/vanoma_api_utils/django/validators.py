from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from vanoma_api_utils.phone_numbers import is_valid_number


def validate_number(phone_number: str) -> None:
    if not is_valid_number(phone_number):
        raise ValidationError(
            _("The value {} is not a valid phone number".format(phone_number))
        )


def validate_numeric(value: str) -> None:
    if not value.isnumeric():
        raise ValidationError(
            _("The value {} is not valid numeric string".format(value))
        )
