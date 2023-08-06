from datetime import datetime


def format_datetime(value: datetime) -> str:
    formatted = value.isoformat()

    if formatted.endswith("+00:00"):
        return formatted[:-6] + "Z"

    return formatted
