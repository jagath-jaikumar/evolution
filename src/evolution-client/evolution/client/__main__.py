import typer

from evolution.client.game import Game

app = typer.Typer(pretty_exceptions_show_locals=False)

@app.command()
def list_games():
    """List all games for the authenticated user"""
    games = Game.list_games()
    for game in games:
        typer.echo(f"Game {game['id']}")

@app.command()
def create_game():
    """Create a new game"""
    game = Game.create_game()
    typer.echo(f"Created game {game['id']}")

@app.command()
def get_game(game_id: str):
    """Get details for a specific game"""
    game = Game.get_game(game_id)
    typer.echo(f"Game {game['id']} details:")
    for key, value in game.items():
        typer.echo(f"{key}: {value}")

@app.command()
def delete_game(game_id: str):
    """Delete a game"""
    Game.delete_game(game_id)
    typer.echo(f"Deleted game {game_id}")

@app.command()
def join_game(game_id: str):
    """Join an existing game"""
    game = Game.join_game(game_id)
    typer.echo(f"Joined game {game['id']}")

@app.command()
def start_game(game_id: str):
    """Start a game"""
    game = Game.start_game(game_id)
    typer.echo(f"Started game {game['id']}")

@app.command()
def make_move(game_id: int):
    """Make a move in the game"""
    result = Game.make_move(game_id)
    typer.echo(f"Move result: {result}")

if __name__ == "__main__":
    app()
