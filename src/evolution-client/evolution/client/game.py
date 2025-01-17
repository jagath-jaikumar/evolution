from evolution.client.utils import make_request
from evolution.client.auth import authenticated
from typing import Optional


class Game:
    """Client SDK for interacting with the Evolution game API"""

    @staticmethod
    @authenticated
    def list_games(*, token: Optional[str] = None) -> list[dict]:
        """List all games for the authenticated user"""
        response = make_request(token, "GET", "/api/game/")
        return response.json()

    @staticmethod
    @authenticated
    def create_game(*, token: Optional[str] = None) -> dict:
        """Create a new game"""
        response = make_request(token, "POST", "/api/game/")
        return response.json()

    @staticmethod
    @authenticated
    def get_game(game_id: str, *, token: Optional[str] = None) -> dict:
        """Get details for a specific game"""
        response = make_request(token, "GET", f"/api/game/{game_id}/")
        return response.json()

    @staticmethod
    @authenticated
    def delete_game(game_id: str, *, token: Optional[str] = None) -> None:
        """Delete a game"""
        make_request(token, "DELETE", f"/api/game/{game_id}/")

    @staticmethod
    @authenticated
    def join_game(game_id: str, *, token: Optional[str] = None) -> dict:
        """Join an existing game"""
        response = make_request(token, "POST", f"/api/game/{game_id}/join/")
        return response.json()

    @staticmethod
    @authenticated
    def start_game(game_id: str, *, token: Optional[str] = None) -> dict:
        """Start a game"""
        response = make_request(token, "POST", f"/api/game/{game_id}/start/")
        return response.json()

    @staticmethod
    @authenticated
    def make_move(game_id: str, *, token: Optional[str] = None) -> dict:
        """Make a move in the game"""
        response = make_request(token, "POST", f"/api/play/{game_id}/make_move/")
        return response.json()
