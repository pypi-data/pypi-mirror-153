import json
from typing import Any, Dict
from django.apps import apps
from pathlib import Path


def load_fixture(name: str) -> Dict[str, Any]:
    for app_config in apps.get_app_configs():
        file_path = f"{app_config.path}/fixtures/{name}"
        if Path(file_path).exists():
            with open(file_path, "r") as rfile:
                return json.load(rfile)

    raise Exception(f"Fixuture {name} not found.")
