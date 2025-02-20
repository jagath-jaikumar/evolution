import typer
from rich import print_json

from evolution.client.meta import load_config, update_config
from evolution.client.utils import make_request

app = typer.Typer()


@app.command()
def list():
    response = make_request("GET", "/api/game/")
    print_json(data=response.json())


@app.command()
def create():
    """Create a new game"""
    response = make_request("POST", "/api/game/")
    print_json(data=response.json())
    update_config("active_game", response.json()["id"])


@app.command()
def get(game_id: str | None = None):
    """Get details for a specific game"""
    if game_id is None:
        config = load_config()
        game_id = config["active_game"]
    response = make_request("GET", f"/api/game/{game_id}/")
    print_json(data=response.json())


@app.command()
def set_active(game_id: str):
    """Set the active game"""
    update_config("active_game", game_id)


@app.command()
def delete(game_id: str):
    """Delete a game"""
    make_request("DELETE", f"/api/game/{game_id}/")
    typer.echo(f"Game {game_id} deleted")


@app.command()
def join(game_id: str):
    """Join an existing game"""
    response = make_request("POST", f"/api/game/{game_id}/join/")
    print_json(data=response.json())


@app.command()
def start(game_id: str):
    """Start a game"""
    response = make_request("POST", f"/api/game/{game_id}/start/")
    print_json(data=response.json())
