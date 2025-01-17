import os
import time
from functools import wraps

import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

class TokenManager:
    _instance = None
    _token = None
    _expires_at = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_valid_token(self):
        if self._token is None or time.time() >= self._expires_at:
            self._refresh_token()
        return self._token

    def _refresh_token(self):
        url = f'https://{AUTH0_DOMAIN}/oauth/token'

        payload = {
            'grant_type': 'client_credentials',
            'client_id': AUTH0_CLIENT_ID,
            'client_secret': AUTH0_CLIENT_SECRET,
            'audience': AUTH0_AUDIENCE,
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self._token = data['access_token']
            # Set expiration 5 minutes before actual expiry to be safe
            self._expires_at = time.time() + data.get('expires_in', 86400) - 300
        except requests.exceptions.RequestException as e:
            print(f'Error fetching token: {e}')
            raise

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token_manager = TokenManager()
        token = token_manager.get_valid_token()
        kwargs['token'] = token
        return func(*args, **kwargs)
    return wrapper

# Example usage
if __name__ == '__main__':
    @authenticated
    def test_auth(token=None):
        print(f'Bearer Token: {token}')
    
    test_auth()