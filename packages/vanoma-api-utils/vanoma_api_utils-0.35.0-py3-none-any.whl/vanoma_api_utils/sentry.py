from typing import Dict


from typing import Dict, Any, Union


def before_send(
    event: Dict[str, Any], hint: Dict[str, Any]
) -> Union[Dict[str, Any], None]:
    """Do not sent events generated in testing environmets to avoid hitting our quota limit."""
    if event["environment"] == "testing":
        return None
    return event
