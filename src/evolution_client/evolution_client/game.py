from evolution_client import _request_api


def new_game(user_id: str):
    response = _request_api(
        "/api/setup/new/",
        "post",
        {"user_id": user_id},
    )
    return response


def join_game(game_id: str, user_id: str):
    response = _request_api(
        "/api/setup/join/",
        "post",
        {"game_id": game_id, "user_id": user_id},
    )
    return response


def start_game(game_id: str):
    response = _request_api(
        "/api/setup/start/",
        "post",
        {"game_id": game_id},
    )
    return response
