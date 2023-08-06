import json
import os
import shutil
from pathlib import Path

from aoricaan_cli.src.models.api_swagger_v2 import swagger_template
from aoricaan_cli.src.models.cloud_formation import get_basic_template
from aoricaan_cli.src.utils.core import copytree
from aoricaan_cli.src.utils.folders import list_path

work_path = Path(os.getcwd())
pipeline_template_name = ''
cfn_definition_template_name = 'projectTemplate.json'
api_definition_template_name = ''


# TODO: Pending for delete
def write_templates(templates_path: Path):
    """
    Write in the project templates files used for new resources.
    :param templates_path:
    :return:
    """
    from aoricaan_cli.templates import templates
    original_templates_path = Path(os.path.dirname(templates.__file__))
    files = ['api_verbs.json', 'lambda.json', 'lambda.txt']
    for file in files:
        shutil.copy(original_templates_path.joinpath(file), templates_path.joinpath(file))


# TODO: Pending for delete
def write_dev_ops_files(path: Path):
    """
    Write all initial files for a new project.
    :param path:
    :return:
    """
    from aoricaan_cli.templates import project
    original_templates_path = Path(os.path.dirname(project.__file__))
    for file in list_path(path=original_templates_path, exclude_filter='__'):
        shutil.copy(original_templates_path.joinpath(file), path.joinpath(file))


# TODO: Pending for delete
def create_all_files_for_initial_project(*, project_name: str,
                                         artifact_bucket: str):
    from aoricaan_cli import templates

    work_path.joinpath(cfn_definition_template_name).write_text(get_basic_template(project_name=project_name,
                                                                                   artifacts_bucket=artifact_bucket))

    src_path = work_path.joinpath('src')
    src_path.mkdir()

    src_path.joinpath('lambdas').mkdir()

    layers_path = src_path.joinpath('layers')
    layers_path.mkdir()

    # TODO:  Write api definition
    src_path.joinpath('api.json').write_text(json.dumps(swagger_template))

    templates_path = work_path.joinpath('utils')
    templates_path.mkdir()

    templates_path = templates_path.joinpath('templates')
    templates_path.mkdir()

    write_templates(templates_path)

    write_dev_ops_files(work_path)

    from_path = Path(os.path.dirname(templates.__file__)).joinpath('layers')
    copytree(from_path, layers_path)


# TODO: Pending for delete
def force_lowercase(value: str) -> str:
    """
    Force any string to lower case.
    :param value: Any string
    :return: a string forced to lowercase
    """
    assert isinstance(value, str)
    return value.lower()
