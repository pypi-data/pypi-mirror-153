from typing import Any, Dict
import os
import jwt
from datetime import datetime, timedelta
from .constants import ROLE


def create_access_token(payload: Dict[str, Any]) -> str:
    return jwt.encode(payload, os.environ["SECRET_KEY"], "HS256")


def create_service_access_token(service_name: str) -> str:
    return create_access_token(
        {
            "sub": service_name,
            "iat": datetime.utcnow(),
            # Service tokens are short-lived since they are generated on-demand
            "exp": datetime.utcnow() + timedelta(seconds=60),
            "roles": [ROLE.SERVICE],
        }
    )
