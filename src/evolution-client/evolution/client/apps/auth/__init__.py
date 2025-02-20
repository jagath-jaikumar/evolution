import typer

from evolution.client.auth import login as auth_login

auth_app = typer.Typer()


@auth_app.command()
def login():
    auth_login()
