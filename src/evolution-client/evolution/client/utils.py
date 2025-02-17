import os
from typing import Any, Dict, Optional

import requests

from evolution.client.auth import AuthenticationError, authenticate


@authenticate
def make_request(
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
) -> requests.Response:
    """
    Makes an HTTP request to the Django backend with authentication.

    Args:
        token: Auth token to use for the request
        method: HTTP method (GET, POST, PUT, DELETE, etc)
        endpoint: API endpoint path
        payload: Optional request body for POST/PUT requests
        params: Optional query parameters

    Returns:
        Response from the API
    """
    base_url = os.getenv("DJANGO_BACKEND_URL")
    url = f"{base_url}{endpoint}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.request(method=method.upper(), url=url, headers=headers, json=payload, params=params)

    if response.status_code == 403:
        raise AuthenticationError("Invalid token")

    response.raise_for_status()

    return response
