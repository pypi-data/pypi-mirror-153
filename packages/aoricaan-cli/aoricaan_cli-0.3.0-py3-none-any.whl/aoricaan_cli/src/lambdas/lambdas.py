import json
import os
import shutil
from pathlib import Path

import typer

from aoricaan_cli.src.utils.api_local import build_files_for_api_local
from aoricaan_cli.src.utils.core import parse_lambda_code, parse_lambda_cfn_configuration, rename_lambda
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.folders import validate_path_not_exist, validate_path_exist, list_path
from aoricaan_cli.src.utils.globals import load_config

app = typer.Typer()

state = {"verbose": False}


@app.command('new')
def new_lambda(name: str = typer.Option(..., help='Name for the new lambda.', prompt=True),
               handler: str = typer.Option('lambda_function.lambda_handler',
                                           help='name of the function file and function name.')):
    """
    Add a new aws lambda structure in the project.
    """
    lambda_path = Path(load_config().project.folders.lambdas).joinpath(name)
    validate_path_not_exist(path=lambda_path, custom_error_message=f'Already exist a lambda named: {name}')
    lambda_path.mkdir()

    lambda_function, lambda_handler = handler.split('.')

    lambda_code = parse_lambda_code(lambda_handler)
    lambda_path.joinpath(f'{lambda_function}.py').write_text(lambda_code)

    lambda_path.joinpath('__init__.py').write_text("")
    # TODO: Read test templates.
    lambda_path.joinpath('test_lambda_function.py').write_text("")

    cfn_config = parse_lambda_cfn_configuration(handler=handler, name=name, path=lambda_path)
    lambda_path.joinpath('configuration.json').write_text(json.dumps({"cfn": cfn_config,
                                                                      "swagger": {}}, indent=2))

    Debug.success(f'{name} was added successfully!')


@app.command('delete')
def new_lambda(name: str = typer.Option(..., help='Lambda name for delete', prompt=True)):
    """
    Delete an existent lambda in the project.

    """
    work_path = Path(load_config().project.folders.lambdas)
    path = work_path.joinpath(name)
    validate_path_exist(path=path)
    typer.confirm('Are you sure you want to delete it?', abort=True)
    shutil.rmtree(path)
    build_files_for_api_local(reload=True)

    Debug.success(f'{name} was deleted successfully!')


@app.command('rename')
def rename(name: str = typer.Option(..., help='Lambda name for rename', prompt=True),
           new_name: str = typer.Option(..., help='New name for lambda', prompt=True)
           ):
    """
    Change the lambda name.
    """
    work_path = Path(load_config().project.folders.lambdas)
    old_path = work_path.joinpath(name)
    validate_path_exist(path=old_path)
    new_path = work_path.joinpath(new_name)
    validate_path_not_exist(path=new_path)
    os.rename(src=old_path, dst=new_path)
    rename_lambda(old_path=old_path, new_path=new_path)

    Debug.success(f'{name} was renamed to {new_name} successfully!')


@app.command('list')
def get_all_lambdas():
    """
    show all lambdas in the project.

    """
    work_path = Path(load_config().project.folders.lambdas)
    lambdas = [[_lambda] for _lambda in list_path(path=work_path, exclude_filter='__') if
               work_path.joinpath(_lambda).is_dir()]

    Debug.table(values=lambdas, headers=["lambda name"])


@app.callback()
def root(ctx: typer.Context, verbose: bool = typer.Option(False, '--verbose', '-v')):
    """
    Manage the lambdas in the project

    """
    if verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
