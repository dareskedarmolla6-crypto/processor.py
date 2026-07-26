import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any


class HTTPClient:
    """
    Low-level HTTP transport layer.

    Responsibilities:
    - Send HTTP requests
    - Handle timeout
    - Handle network errors
    - Handle transient connection retries
    - Return raw responses

    It does NOT contain:
    - Trading logic
    - Market decisions
    - Portfolio logic
    """

    def __init__(
        self,
        timeout: int = 20,
        retries: int = 3,
        retry_delay: int = 3
    ):
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

    def get(
        self,
        url: str,
        headers: Dict[str, str] | None = None
    ) -> Dict[str, Any]:
        """
        Execute HTTP GET request with transient failure retry.
        """
        request = urllib.request.Request(
            url,
            headers=headers or {}
        )

        last_error = None

        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(
                    request,
                    timeout=self.timeout
                ) as response:
                    return {
                        "status": response.status,
                        "body": response.read()
                    }
            except (urllib.error.URLError, TimeoutError) as error:
                last_error = error
                if attempt < self.retries - 1:
                    time.sleep(self.retry_delay)
                    continue

        raise ConnectionError(
            f"HTTP request failed after {self.retries} attempts: {last_error}"
        )

    def post(
        self,
        url: str,
        headers: Dict[str, str] | None = None,
        data: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Execute HTTP POST request.

        Low level transport only.
        Does NOT contain business logic.
        """
        encoded_data = urllib.parse.urlencode(
            data or {}
        ).encode()

        request = urllib.request.Request(
            url,
            data=encoded_data,
            headers=headers or {},
            method="POST"
        )

        last_error = None

        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(
                    request,
                    timeout=self.timeout
                ) as response:
                    return {
                        "status": response.status,
                        "body": response.read()
                    }
            except urllib.error.HTTPError as error:
                body = error.read().decode()

                return {
                    "status": error.code,
                    "body": body
                }

            except (urllib.error.URLError, TimeoutError) as error:
                last_error = error
                if attempt < self.retries - 1:
                    time.sleep(self.retry_delay)
                    continue

        raise ConnectionError(
            f"HTTP POST failed after {self.retries} attempts: {last_error}"
        )
