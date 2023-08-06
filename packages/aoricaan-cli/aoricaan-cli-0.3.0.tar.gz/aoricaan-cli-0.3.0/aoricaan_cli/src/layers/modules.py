import shutil
from pathlib import Path

import typer

from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.folders import validate_path_exist, validate_path_not_exist, list_path, rename_path
from aoricaan_cli.src.utils.globals import load_config

app = typer.Typer()


@app.command('add')
def add_new_module(layer: str = typer.Option(..., help='Name of an existing layer', prompt='Layer name'),
                   module: str = typer.Option(..., help='Name for the new module', prompt='Module name')):
    """
    Add a new module in an existent layer.
    """
    work_path = Path(load_config().project.folders.layers)
    layer_path = work_path.joinpath(layer)
    validate_path_exist(path=layer_path, custom_error_message=f'The layer: {layer} not exist')
    new_module_path = layer_path.joinpath('python').joinpath(module)
    validate_path_not_exist(path=new_module_path,
                            custom_error_message=f'The module: {module} already exist in the layer {layer}')
    new_module_path.mkdir()
    new_module_path.joinpath('__init__.py').write_text("")


@app.command('rename')
def rename_module(layer: str = typer.Option(..., help='Name of an existing layer', prompt='Layer name'),
                  module_name: str = typer.Option(..., help='Name of an existent module', prompt='Module name'),
                  new_module_name: str = typer.Option(..., help='New name for the module', prompt='Module name')):
    """
    Rename a module in an existent layer.
    """
    work_path = Path(load_config().project.folders.layers)
    layer_path = work_path.joinpath(layer)
    validate_path_exist(path=layer_path, custom_error_message=f'The layer: {layer} not exist')

    old_module_path = layer_path.joinpath('python').joinpath(module_name)
    validate_path_exist(path=old_module_path, custom_error_message=f'The module: {module_name} not exist')

    new_module_path = layer_path.joinpath('python').joinpath(new_module_name)
    validate_path_not_exist(path=new_module_path, custom_error_message=f'The module: {new_module_name} already exist')

    typer.confirm(
        "when renaming the module you need to update all imports where it is being used.\nAre you sure about this?",
        abort=True)

    rename_path(src=old_module_path, dst=new_module_path)


@app.command('delete')
def delete_module(layer: str = typer.Option(..., help='Name of an existing layer', prompt='Layer name'),
                  module_name: str = typer.Option(..., help='Name of an existent module', prompt='Module name')):
    """
    Delete an existent module.
    """
    work_path = Path(load_config().project.folders.layers)
    layer_path = work_path.joinpath(layer)
    validate_path_exist(path=layer_path, custom_error_message=f'The layer: {layer} not exist')

    module_path = layer_path.joinpath('python').joinpath(module_name)
    validate_path_exist(path=module_path, custom_error_message=f'The module: {module_name} not exist in the layer {layer}')

    typer.confirm('Are you sure delete it?', abort=True)

    shutil.rmtree(module_path)


@app.command('list')
def list_modules(layer: str = typer.Option(..., help='Name of an existing layer', prompt='Layer name')):
    """
    List all modules inside the layer.
    """
    work_path = Path(load_config().project.folders.layers)
    layer_path = work_path.joinpath(layer)
    validate_path_exist(path=layer_path, custom_error_message=f'The layer: {layer} not exist')
    modules_path = layer_path.joinpath('python')
    modules = [[n] for n in list_path(path=modules_path, exclude_filter='__') if modules_path.joinpath(n).is_dir()]
    Debug.table(values=modules, headers=[f'Modules: {layer}'])


@app.callback()
def root():
    """
    Manage the modules inside in a existent layer
    """


if __name__ == '__main__':
    app()
