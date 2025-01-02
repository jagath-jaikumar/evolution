from evolution_client import _request_api


def get_game(game_id: str):
    response = _request_api(
        "/api/observe/game/",
        "get",
        {"game_id": game_id},
    )
    return response
