import shutil
from pathlib import Path

import typer

from aoricaan_cli.src.layers import modules
from aoricaan_cli.src.utils.core import copytree, add_new_layer_definition, delete_layer_definition, \
    rename_layer_definition
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.folders import validate_path_not_exist, validate_path_exist, list_path
from aoricaan_cli.src.utils.globals import load_config
from aoricaan_cli.src.utils.state import State

state = State()
app = typer.Typer()
app.add_typer(modules.app, name='module')


@app.command('new')
def new_layer(name: str = typer.Option(..., help='Name of the layer', prompt='Layer name: ')):
    """
    create a new structure layer.

    """
    work_path = Path(load_config().project.folders.layers)
    new_layer_path = work_path.joinpath(name)
    validate_path_not_exist(path=new_layer_path, custom_error_message=f'Already exist a layer with the name: {name}')
    new_layer_path.mkdir()
    new_layer_path.joinpath('python').mkdir()
    add_new_layer_definition(name)

    Debug.success("The new layer was added successfully!")


@app.command('delete')
def delete_layer(name: str = typer.Option(..., help='Name of the layer', prompt='Layer name: ')):
    """
    Delete an existent layer.

    """
    work_path = Path(load_config().project.folders.layers)
    _layer_path = work_path.joinpath(name)
    validate_path_exist(path=_layer_path, custom_error_message=f'Not exist the layer {name}')
    typer.confirm('Are you sure delete it?', abort=True)
    shutil.rmtree(_layer_path)
    delete_layer_definition(name)

    Debug.success("The layer was deleted successfully!")


@app.command('rename')
def rename(name: str = typer.Option(..., help='Name of the layer', prompt='Layer name: '),
           new_name: str = typer.Option(..., help='New name of the layer', prompt='New layer name: ')):
    """
    Rename an existent layer.

    """
    work_path = Path(load_config().project.folders.layers)
    old_layer_path = work_path.joinpath(name)
    validate_path_exist(path=old_layer_path, custom_error_message=f'Not exist the layer {name}')
    new_layer_path = work_path.joinpath(new_name)
    validate_path_not_exist(path=new_layer_path, custom_error_message=f'Already exist a layer with the name: {name}')
    typer.confirm(
        "when renaming the layer you need to update all imports where it is being used.\nAre you sure about this?",
        abort=True)
    copytree(src=old_layer_path, dst=new_layer_path)
    shutil.rmtree(old_layer_path)
    rename_layer_definition(src=name, dst=new_name)

    Debug.success("The layer was renamed successfully!")


@app.command('list')
def list_layer():
    """
    list all layers in the project

    """
    work_path = Path(load_config().project.folders.layers)
    values = [[n] for n in list_path(path=work_path, exclude_filter='__')]
    Debug.table(values=values, headers=['Layer name'])


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the layers in the project.

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
