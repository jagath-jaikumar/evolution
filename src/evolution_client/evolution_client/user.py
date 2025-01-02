from evolution_client import _request_api


def register_user(username: str, password: str, email: str):
    response = _request_api(
        "/register/",
        "post",
        {
            "username": username,
            "password": password,
            "email": email,
        },
    )
    return response


def get_user_id_from_username(username: str):
    response = _request_api(
        "/get_user_id/",
        "get",
        {"username": username},
    )
    return response
