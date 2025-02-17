import typer

from evolution.client.apps.auth import auth_app
from evolution.client.apps.game import app as game_app

app = typer.Typer()

app.add_typer(auth_app, name="auth")
app.add_typer(game_app, name="game")

if __name__ == "__main__":
    app()
