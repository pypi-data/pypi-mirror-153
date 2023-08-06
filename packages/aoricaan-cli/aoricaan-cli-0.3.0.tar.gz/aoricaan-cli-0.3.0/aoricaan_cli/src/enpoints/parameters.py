import typer

from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.state import State

state = State()
app = typer.Typer()


@app.command('add')
def add_parameter():
    """
    Add a new param in a existent endpoint

    """
    pass


@app.command('update')
def update_parameter():
    """
    Update some parameter in a existent endpoint

    """
    pass


@app.command('delete')
def delete_parameter():
    """
    Delete the parameter defined.

    """
    pass


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the parameter definition in some endpoint.

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
