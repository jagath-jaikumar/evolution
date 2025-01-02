from evolution_client import _request_api


def get_game(game_id: str):
    response = _request_api(
        "/api/observe/game/",
        "get",
        {"game_id": game_id},
    )
    return response


def get_player(game_id: str, player_id: str):
    response = _request_api(
        "/api/observe/player/",
        "get",
        {"game_id": game_id, "player_id": player_id},
    )
    return response
