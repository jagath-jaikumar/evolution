import typer
from rich import print_json

from evolution.client.utils import make_request
from evolution.client.meta import update_config, load_config
from evolution.client.auth import login as auth_login

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def list_games():
    response = make_request("GET", "/api/game/")
    print_json(data=response.json())


@app.command()
def create_game():
    """Create a new game"""
    response = make_request("POST", "/api/game/")
    print_json(data=response.json())
    update_config("active_game", response.json()["id"])

@app.command()
def get_active_game():
    config = load_config()
    print(config["active_game"])

@app.command()
def get_game(game_id: str):
    """Get details for a specific game"""
    response = make_request("GET", f"/api/game/{game_id}/")
    print_json(data=response.json())

@app.command()
def set_active_game(game_id: str):
    """Set the active game"""
    update_config("active_game", game_id)

@app.command()
def delete_game(game_id: str):
    """Delete a game"""
    make_request("DELETE", f"/api/game/{game_id}/")


@app.command()
def join_game(game_id: str):
    """Join an existing game"""
    response = make_request("POST", f"/api/game/{game_id}/join/")
    print_json(data=response.json())


@app.command()
def start_game(game_id: str):
    """Start a game"""
    response = make_request("POST", f"/api/game/{game_id}/start/")
    print_json(data=response.json())


@app.command()
def login():
    auth_login()


if __name__ == "__main__":
    app()
