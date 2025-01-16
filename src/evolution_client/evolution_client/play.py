from evolution_client.game import _request_api


def basic_action(game_id: str, player_id: str, action: str):
    response = _request_api(
        "/api/play/basic_action/",
        "post",
        {"game_id": game_id, "player_id": player_id, "action": action},
    )
    return response
