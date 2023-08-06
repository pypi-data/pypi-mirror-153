import phonenumbers  # type: ignore


class InvalidPhoneNumber(Exception):
    pass


def is_valid_number(phone_number: str) -> bool:
    if not phone_number:
        return False

    striped_number = str(phone_number).strip()

    if not striped_number.isnumeric():
        return False

    if striped_number.startswith("+"):
        return False

    try:
        # All phone numbers must be in international format with the + sign
        parsed_number = phonenumbers.parse("+{}".format(striped_number), None)
        # TODO (1): Check country code based on the market vanoma is running in.
        # TODO (2): We can truly check for number validity but we are skipping it - https://github.com/daviddrysdale/python-phonenumbers
        return parsed_number.country_code == 250
    except phonenumbers.NumberParseException:
        return False
