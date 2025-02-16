import os
import requests
import typer
import time
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
import jwt
import json
from rich import print
import base64

APP_DIR = ".evolution"

HOME_DIR = os.path.expanduser("~")
TOKEN_DIR = os.path.join(HOME_DIR, APP_DIR)
TOKEN_FILE = os.path.join(TOKEN_DIR, "tokens.json")
ENCODE_TOKENS = True
os.makedirs(TOKEN_DIR, exist_ok=True)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS = ['RS256']

class AuthenticationError(Exception):
    pass


def persist_tokens(token_data: dict) -> None:
    # Simple base64 encoding of the token data
    if ENCODE_TOKENS:
        encoded = json.dumps(token_data).encode('utf-8')
        encoded_data = base64.b64encode(encoded).decode('utf-8')
    else:
        encoded_data = json.dumps(token_data)
    with open(TOKEN_FILE, "w") as f:
        json.dump({"data": encoded_data}, f)

def load_tokens() -> dict | None:
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        encoded_data = json.load(f)["data"]
        if ENCODE_TOKENS:
            # Decode the base64 encoded data
            decoded = base64.b64decode(encoded_data.encode('utf-8'))
            return json.loads(decoded)
        else:
            return json.loads(encoded_data)



def authenticate(func):
    """
    Decorator that authenticates the user and passes the access token to the wrapped function
    """
    def wrapper(*args, **kwargs):
        token_data = load_tokens()
        if token_data:
            validate_token(token_data['id_token'])
        else:
            token_data = login()
            
        return func(*args, token=token_data['access_token'], **kwargs)
        
    return wrapper


def login() -> dict | None:
    """
    Runs the device authorization flow and stores the user object in memory
    """
    device_code_payload = {
        'client_id': AUTH0_CLIENT_ID,
        'scope': 'openid profile',
        'audience': AUTH0_AUDIENCE
    }
    device_code_response = requests.post(f'https://{AUTH0_DOMAIN}/oauth/device/code', data=device_code_payload)

    if device_code_response.status_code != 200:
        print('Error generating the device code')
        raise typer.Exit(code=1)

    print('Logging in...')
    device_code_data = device_code_response.json()
    typer.launch(device_code_data['verification_uri_complete'])
    print('1. On your computer or mobile device navigate to: ', device_code_data['verification_uri_complete'])
    print('2. Enter the following code: ', device_code_data['user_code'])
    token_payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code_data['device_code'],
        'client_id': AUTH0_CLIENT_ID
    }

    authenticated = False
    while not authenticated:
        # Checking if the user completed the flow
        token_response = requests.post('https://{}/oauth/token'.format(AUTH0_DOMAIN), data=token_payload)

        token_data = token_response.json()
        if token_response.status_code == 200:
            print('Authenticated!')
            validate_token(token_data['id_token'])
            persist_tokens(token_data)
            authenticated = True
            return token_data
        elif token_data['error'] not in ('authorization_pending', 'slow_down'):
            print(token_data['error_description'])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data['interval'])


def validate_token(id_token):
    """
    Verify the token and its precedence

    :param id_token:
    """
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    issuer = f'https://{AUTH0_DOMAIN}/'
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=AUTH0_CLIENT_ID)
    tv.verify(id_token)
