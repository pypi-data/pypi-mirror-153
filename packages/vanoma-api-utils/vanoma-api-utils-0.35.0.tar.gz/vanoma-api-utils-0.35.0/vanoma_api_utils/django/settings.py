import os
import dj_database_url  # type: ignore
from typing import Any, Dict
from ..misc import resolve_environment


def resolve_database() -> Dict[str, str]:
    if resolve_environment() == "testing":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join("/tmp", "db.sqlite3"),
        }

    return dj_database_url.config(conn_max_age=600)


def resolve_logging() -> Dict[str, Any]:
    if resolve_environment() == "testing":
        return {}

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {  # Needed to prettify logs (especially for mini-huey/background task queue) to match gunicon logs format.
                "style": "{",
                "format": "[{asctime}] [{process}] [{levelname}] {message}",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }


def resolve_file_storage() -> str:
    if resolve_environment() == "testing":
        return "django.core.files.storage.FileSystemStorage"

    return "storages.backends.s3boto3.S3Boto3Storage"
