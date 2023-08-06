__version__ = "0.1.1"

import json
from typing import Any, Dict
from unittest.mock import patch

from flask.testing import FlaskClient
from urllib3.util import parse_url
from werkzeug.test import TestResponse


class ConvertHttpx2FlaskTestClient(FlaskClient):
    def __init__(self, *args: Any,
                 base_url: str = "http://localhost",
                 headers: Dict[str, str] = None,
                 cookies: Dict[str, Any] = None,
                 timeout: float = 10.0,
                 verify_ssl: bool = True,
                 **kwargs: Any):
        self.base_url = base_url
        self._headers = headers if headers else {}
        self._cookies = cookies if cookies else {}
        self._timeout = timeout
        self.verify_ssl = verify_ssl

        self.mock_httpx_request = patch("httpx.Client.request",
                                        side_effect=self._convert_httpx_request_2_flask_client_open)

        super().__init__(*args, **kwargs)

    def get_headers(self):
        return self._headers

    def _convert_httpx_request_2_flask_client_open(self, *args, **kwargs):
        url = parse_url(kwargs.pop("url"))
        kwargs["base_url"] = self.base_url
        kwargs["path"] = url.path
        kwargs.pop("content")
        kwargs.pop("files")
        kwargs.pop("params")
        try:
            resp = self.open(*args, **kwargs)
        except Exception as err:
            resp = TestResponse(
                response=json.dumps({"error_type": str(err.__class__), "args": err.args}).encode(),
                status="500",
                headers={"Content-Type": "application/json"},
                request=None)
        resp.content = resp.data

        # Make `resp.json` return the method resp.get_json, instead of the result resp.get_json()
        resp._get_json = resp.get_json
        resp.get_json = lambda: resp._get_json

        return resp

    def get_cookies(self):
        return self._cookies

    def get_timeout(self):
        return self._timeout

    def __enter__(self) -> "FlaskClient":
        self.mock_httpx_request.start()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_httpx_request.stop()
        return super().__exit__(exc_type, exc_val, exc_tb)

