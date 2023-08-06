from importlib.metadata import version as v

import typer
from dotenv import load_dotenv

from aoricaan_cli.src.api import local
from aoricaan_cli.src.enpoints import endpoints
from aoricaan_cli.src.lambdas import lambdas
from aoricaan_cli.src.layers import layers
from aoricaan_cli.src.project import project

load_dotenv()

app = typer.Typer()
app.add_typer(endpoints.app, name='endpoint')
app.add_typer(lambdas.app, name='lambda')
app.add_typer(layers.app, name='layers')
app.add_typer(local.app, name='api')
app.add_typer(project.app, name='project')


@app.callback(invoke_without_command=True)
def callback_version(version: bool = False):
    """
    Prints the version of the CLI.
    """
    if version:
        typer.echo(f'version: {v("aoricaan-cli")}')
