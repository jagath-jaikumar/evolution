import logging
import time
from functools import lru_cache

import requests
from django.contrib.auth.models import User
from django.core.cache import cache
from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from evolution.authentication.constants import ALGORITHMS, API_IDENTIFIER, AUTH0_DOMAIN

logger = logging.getLogger(__name__)


# Cache public keys for 1 hour since they rarely change
@lru_cache(maxsize=1)
def get_public_key():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    try:
        jwks = requests.get(jwks_url, timeout=5).json()
        return {key["kid"]: key for key in jwks["keys"]}
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch public keys: {e}")
        return {}


# Cache user info for 5 minutes to reduce Auth0 API calls
def get_user_info(token):
    cache_key = f"userinfo_{token[:32]}"  # Use part of token as cache key
    cached_info = cache.get(cache_key)
    if cached_info:
        return cached_info

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    try:
        response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {token}"}, timeout=5)
        if response.status_code != 200:
            raise AuthenticationFailed("Failed to fetch user info")
        user_info = response.json()
        cache.set(cache_key, user_info, 300)  # Cache for 5 minutes
        return user_info
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch user info: {e}")
        raise AuthenticationFailed("Failed to fetch user info")


class Auth0Authentication(BaseAuthentication):
    def authenticate(self, request):
        start = time.perf_counter()
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Decode and validate the token
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = get_public_key().get(unverified_header["kid"])
            if not rsa_key:
                raise AuthenticationFailed("Invalid token header")

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )

            username = payload.get("sub")
            if not username:
                raise AuthenticationFailed("No sub claim in token")

            # Cache user objects to reduce database queries
            cache_key = f"auth0_user_{username}"
            user = cache.get(cache_key)

            if not user:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user_info = get_user_info(token)
                    user = User.objects.create(
                        username=username,
                        first_name=user_info.get("given_name"),
                        last_name=user_info.get("family_name"),
                    )
                    user.set_unusable_password()
                    user.save()

                cache.set(cache_key, user, 300)  # Cache user for 5 minutes

            duration = time.perf_counter() - start
            logger.debug(f"Authentication took {duration:.2f} seconds to process.")
            return (user, None)

        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise AuthenticationFailed("Token has expired")
        except jwt.JWTClaimsError:
            logger.error("Incorrect claims, please check audience and issuer")
            raise AuthenticationFailed("Incorrect claims, please check audience and issuer")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed(f"Authentication failed: {str(e)}")
