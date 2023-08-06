import os
from pathlib import Path

import typer

from aoricaan_cli import templates
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.globals import load_config
from aoricaan_cli.src.utils.install_layers import install
from aoricaan_cli.src.utils.state import State
from aoricaan_cli.src.utils.synth import build_all_lambdas, update_deploy_id_resource_api_gateway, build_layers
from aoricaan_cli.src.utils.templates_generator import generate_standard_template, generate_templates

state = State()
app = typer.Typer()


@app.command('synth')
def build_project():
    """
    Build the files for deploy the project in aws.
    """
    configuration = load_config()
    template_paths = [Path(path) for path in configuration.templates.deploy.project_template]
    api_paths = [Path(path) for path in configuration.templates.deploy.api_swagger_template]

    lambdas_path = Path(configuration.project.folders.lambdas)
    layers_path = Path(configuration.project.folders.layers)

    build_all_lambdas(lambdas_path=lambdas_path, path_cfn_template=template_paths,
                      path_swagger_template=api_paths, bucket=os.environ.get('artifact_bucket'))
    update_deploy_id_resource_api_gateway(paths_template=template_paths)
    build_layers(layers_path=layers_path)


@app.command('install')
def install_layers():
    """
    Install layer in local environment.
    """
    install(layers_path=Path(load_config().project.folders.layers))


@app.command('init')
def initialize_new_project(default: bool = typer.Option(False,
                                                        help="Create a new project with default template.",
                                                        prompt="Do you want to create a new project with "
                                                               "default template?")):
    """
    Initialize a new empty project in the current path.

    """
    if default:
        generate_standard_template()
    else:
        Debug.info('Remember the project will be compatible with cookiecutter.')
        template = typer.prompt("path to template: ")
        generate_templates(template)
    Debug.success('Project init successfully!')


@app.command('show')
def show_path():
    print(os.path.dirname(templates.__file__))


@app.callback()
def root(ctx: typer.Context, verbose: bool = False):
    """
    Manage the project.

    """
    state.verbose = verbose
    if state.verbose and ctx.invoked_subcommand:
        Debug.info(f"Running command: {ctx.invoked_subcommand}")


if __name__ == '__main__':
    app()
