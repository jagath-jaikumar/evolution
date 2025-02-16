import typer

from evolution.client.utils import make_request

app = typer.Typer(pretty_exceptions_show_locals=False)

@app.command()
def list_games():
    response = make_request("GET", "/api/game/")
    return response.json()

@app.command()
def create_game():
    """Create a new game"""
    response = make_request("POST", "/api/game/")
    return response.json()

@app.command()
def get_game(game_id: str):
    """Get details for a specific game"""
    response = make_request("GET", f"/api/game/{game_id}/")
    return response.json()

@app.command()
def delete_game(game_id: str):
    """Delete a game"""
    make_request("DELETE", f"/api/game/{game_id}/")

@app.command()
def join_game(game_id: str):
    """Join an existing game"""
    response = make_request("POST", f"/api/game/{game_id}/join/")
    return response.json()

@app.command()
def start_game(game_id: str):
    """Start a game"""
    response = make_request("POST", f"/api/game/{game_id}/start/")
    return response.json()

@app.command()
def test_auth():
    from evolution.client.auth import login
    login()
    

if __name__ == "__main__":
    app()
