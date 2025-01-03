import os

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TIMEOUT = 10
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}


def _request_api(path: str, method: str, data: dict = None):
    try:
        kwargs = {"timeout": TIMEOUT, "headers": HEADERS}

        if method.upper() == "GET":
            kwargs["params"] = data
        else:
            kwargs["json"] = data

        response = requests.request(method, f"{BASE_URL}/{path}", **kwargs)
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("Request timed out")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
