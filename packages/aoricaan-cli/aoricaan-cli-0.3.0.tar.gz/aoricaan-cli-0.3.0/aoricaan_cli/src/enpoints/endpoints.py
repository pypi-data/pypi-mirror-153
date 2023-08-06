import json
from pathlib import Path

import typer

from aoricaan_cli.src.enpoints import parameters
from aoricaan_cli.src.utils.api_local import build_files_for_api_local
from aoricaan_cli.src.utils.core import (load_all_endpoints,
                                         delete_endpoint,
                                         add_endpoint_to_lambda_existent,
                                         rename_endpoint, parse_lambda_code, parse_lambda_cfn_configuration,
                                         parse_lambda_swagger_configuration, validate_if_exist_verb_in_endpoint)
from aoricaan_cli.src.utils.data_types import Verbs, endpoint_name_validation
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.folders import validate_path_not_exist, validate_path_exist
from aoricaan_cli.src.utils.globals import load_config
from aoricaan_cli.src.utils.state import State

app = typer.Typer()
app.add_typer(parameters.app, name='param')

state = State()


def set_default_path(value: Path):
    if not value or value.name == '':
        return Path(load_config().project.folders.lambdas)
    return value


# TODO: Validar que no exista el mismo endpoint/verbo

@app.command('new')
def new_endpoint(lambda_name: str = typer.Option(..., help='Lambda name where is the endpoint.',
                                                 prompt='Ingress the lambda name'),
                 handler: str = typer.Option('lambda_function.lambda_handler',
                                             help='name of the function file and function name.'),
                 endpoint: str = typer.Option(..., help='Name for the endpoint',
                                              callback=endpoint_name_validation,
                                              prompt='Ingress the endpoint name'),
                 verb: Verbs = typer.Option(..., help='Name of the verb for the endpoint',
                                            prompt='Ingress the verb fot this endpoint'),
                 cors: bool = typer.Option(False, help='Enable the cors for the endpoint', prompt='Enable cors?')):
    """
    Add a new lambda with the swagger configuration to create an endpoint.

    """
    lambdas_work_path = Path(load_config().project.folders.lambdas)
    lambda_path = lambdas_work_path.joinpath(lambda_name)
    validate_path_not_exist(path=lambda_path, custom_error_message=f'Already exist a lambda named: {lambda_name}')
    validate_if_exist_verb_in_endpoint(verb=verb, endpoint=endpoint)
    lambda_path.mkdir()

    lambda_function, lambda_handler = handler.split('.')
    lambda_code = parse_lambda_code(lambda_handler)
    lambda_path.joinpath(f'{lambda_function}.py').write_text(lambda_code)

    lambda_path.joinpath('__init__.py').write_text("")
    lambda_path.joinpath('test_lambda_function.py').write_text("")

    cfn_config = parse_lambda_cfn_configuration(handler=handler, name=lambda_name, path=lambda_path)
    swagger_config = parse_lambda_swagger_configuration(verb=verb, lambda_name=lambda_name, endpoint=endpoint,
                                                        cors=cors)
    lambda_path.joinpath('configuration.json').write_text(json.dumps({"cfn": cfn_config,
                                                                      "swagger": swagger_config}))

    build_files_for_api_local(reload=True)

    Debug.success(f"The endpoint: {endpoint} and the lambda: {lambda_name} was created")


@app.command('add')
def add_endpoint(lambda_name: str = typer.Option(..., help='Lambda name where is the endpoint.',
                                                 prompt='Ingress the lambda name'),
                 endpoint: str = typer.Option(..., help='Name for the endpoint',
                                              callback=endpoint_name_validation,
                                              prompt='Ingress the endpoint name'),
                 verb: Verbs = typer.Option(..., help='Name of the verb for the endpoint',
                                            prompt='Ingress the verb fot this endpoint'),
                 cors: bool = typer.Option(False, help='Enable the cors for the endpoint', prompt='Enable cors?'),
                 path: Path = typer.Option('', callback=set_default_path, help='Path to the lambda folder')):
    """
    Add the swagger configuration for a new endpoint on existent lambda.

    """
    validate_if_exist_verb_in_endpoint(verb=verb, endpoint=endpoint)
    add_endpoint_to_lambda_existent(lambda_name=lambda_name,
                                    endpoint=endpoint,
                                    verb=verb,
                                    cors=cors,
                                    path=path)
    build_files_for_api_local(reload=True)
    Debug.success('Endpoint was added')


@app.command('rename')
def rename(lambda_name: str = typer.Option(..., help='Lambda name where is the endpoint.',
                                           prompt='Ingress the lambda name'),
           new_endpoint_name: str = typer.Option(..., help='Name for the endpoint',
                                                 callback=endpoint_name_validation,
                                                 prompt='Ingress the endpoint name')):
    """
    Update the endpoint name.
    """
    lambdas_work_path = Path(load_config().project.folders.lambdas)
    path = lambdas_work_path.joinpath(lambda_name)
    validate_path_exist(path=path, custom_error_message=f'lambda {lambda_name} does not exist.')
    rename_endpoint(path=path, new_endpoint=new_endpoint_name)

    Debug.success(f'The endpoint for the lambda {lambda_name} now is {new_endpoint_name}!')


@app.command('delete')
def new_endpoint(lambda_name: str = typer.Option(..., help='Lambda name where is the endpoint.',
                                                 prompt='Ingress the lambda name'),
                 path: Path = typer.Option('', callback=set_default_path, help='Path to the lambda folder')):
    """
    Delete the swagger configuration on existent lambda.

    """
    typer.confirm('Are you sure you want to delete it?', abort=True)
    delete_endpoint(lambda_name=lambda_name, path=path)
    build_files_for_api_local(reload=True)
    Debug.success('Endpoin was deleted')


@app.command('list')
def get_all_endpoints(path: Path = typer.Option('', callback=set_default_path, help='Path to the lambda folder')):
    """
    show a list with all lambdas in the project.

    """
    result = [[lambda_name, verb, endpoint] for endpoint, verb, lambda_name in load_all_endpoints(path) if endpoint]
    Debug.table(values=result, headers=["Lambda name", "verb", "endpoint"])


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the endpoints in the project

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
