import json
import requests
import allure

class BaseClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        # Log request to Allure report
        request_body = kwargs.get("json") or kwargs.get("data")
        allure.attach(
            json.dumps(request_body, indent=2) if isinstance(request_body, dict) else str(request_body or "None"),
            name=f"Request Body [{method} {url}]",
            attachment_type=allure.attachment_type.JSON
        )

        response = self.session.request(method, url, **kwargs)

        # Log response to Allure report
        allure.attach(
            response.text or "<empty response>",
            name=f"Response Body [Status {response.status_code}]",
            attachment_type=allure.attachment_type.JSON
        )

        return response