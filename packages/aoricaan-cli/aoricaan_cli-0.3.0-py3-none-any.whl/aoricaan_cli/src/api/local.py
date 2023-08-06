import typer

from aoricaan_cli.src.utils.api_local import build_and_run
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.state import State

state = State()

app = typer.Typer()


@app.command('run')
def run_api_local():
    """
    Run the api in a local environment.

    """
    build_and_run()


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the Api in local environment.

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
