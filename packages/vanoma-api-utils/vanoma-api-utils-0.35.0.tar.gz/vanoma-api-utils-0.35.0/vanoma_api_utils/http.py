import json
import logging
import requests
from typing import Any, Dict, Union
from requests import Response


class Client(object):
    def __init__(self) -> None:
        self.timeout = 20  # 20 seconds to match java client
        self.session = requests.Session()

    def get(self, url: str, headers: Dict[str, Any] = None) -> Response:
        return self._request("GET", url, None, headers)

    def post(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any] = None
    ) -> Response:
        return self._request("POST", url, data, headers)

    def put(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any] = None
    ) -> Response:
        return self._request("PUT", url, data, headers)

    def patch(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any] = None
    ) -> Response:
        return self._request("PATCH", url, data, headers)

    def delete(self, url: str, headers: Dict[str, Any] = None) -> Response:
        return self._request("DELETE", url, None, headers)

    def _request(
        self,
        method: str,
        url: str,
        data: Union[Dict[str, Any], None],
        headers: Union[Dict[str, Any], None],
    ) -> Response:
        response = self.session.request(method, url, json=data, headers=headers)

        if not response.ok:
            # Using the same logging format as what we use in java http client to simplify searching logs.
            logging.error(
                f"Unexpected response code from: {method} {url} {response.status_code}. RequestBody={json.dumps(data)}. ResponseBody={response.content.decode()}."
            )

        return response


client = Client()
