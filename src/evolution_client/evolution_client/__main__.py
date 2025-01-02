import inspect

import typer

import evolution_client.game as game
import evolution_client.user as user
import evolution_client.observe as observe

app = typer.Typer()


def register_commands(module):
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if not name.startswith("_"):

            @app.command(name=name.replace("_", "-"))
            def command_wrapper(*args, func=func, **kwargs):
                result = func(*args, **kwargs)
                print(result)

            # Copy the original function's signature to the wrapper
            command_wrapper.__signature__ = inspect.signature(func)


# Register commands from game and user modules
register_commands(game)
register_commands(user)
register_commands(observe)

if __name__ == "__main__":
    app()
