import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

import typer

from aoricaan_cli.src.utils.data_types import Verbs
from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.globals import load_config
from aoricaan_cli.src.utils.str_parser import snake_case_or_kebab_case_to_pascal_case

utils_templates_path = Path('utils/templates')
path_lambda_configuration = utils_templates_path.joinpath('lambda.json')
path_lambda_template = utils_templates_path.joinpath('lambda.txt')
path_lambda_swagger = utils_templates_path.joinpath('api_verbs.json')

configuration_name = 'configuration.json'

FN_SUB = "Fn::Sub"


def create_lambda_configuration(*, new_lambda_folder: Path, handler: str, name: str):
    cfn_lambda = json.loads(path_lambda_configuration.read_text())
    _cfn_lambda = cfn_lambda
    _cfn_lambda['Properties']['FunctionName'][FN_SUB] = "${Environment}-" + name
    _cfn_lambda['Properties']['Code'] = str(new_lambda_folder).replace(os.sep, "/")
    _cfn_lambda['Properties']['Handler'] = handler
    return _cfn_lambda


def create_swagger_configuration(*, lambda_name: str, endpoint: str, verb: str, cors: bool):
    swagger = json.loads(path_lambda_swagger.read_text())
    configuration = {
        endpoint: {verb: parse_api_verb_definition(name=lambda_name, swagger_definition=swagger['definition'])}}

    if cors:
        configuration[endpoint].update({
            'options': swagger['options']
        })

    return configuration


def create_lambda_files(new_lambda_folder: Path):
    new_lambda_folder.joinpath('__init__.py').write_text("", encoding='utf-8')
    new_lambda_folder.joinpath('test_lambda_function.py').write_text("", encoding='utf-8')
    new_lambda_folder.joinpath('lambda_function.py').write_text(path_lambda_template.read_text(),
                                                                encoding='utf-8')


def create_only_cfn_configuration(new_lambda_folder: Path, cfn_configuration: Dict[str, Any]):
    __save_configuration(path=new_lambda_folder, cfn_configuration=cfn_configuration)


def create_endpoint_configuration(new_lambda_folder: Path, swagger_configuration: Dict[str, Any],
                                  cfn_configuration: Dict[str, Any]):
    __save_configuration(path=new_lambda_folder, swagger_configuration=swagger_configuration,
                         cfn_configuration=cfn_configuration)


def __save_configuration(*, path: Path, swagger_configuration: Optional[Dict[str, Any]] = None,
                         cfn_configuration: Optional[Dict[str, Any]] = None):
    path.joinpath(configuration_name).write_text(json.dumps(
        {"swagger": swagger_configuration or {}, "cfn": cfn_configuration or {}}, indent=2
    ), encoding='utf-8')


def get_all_lambdas_folder_name(path: Path):
    for folder in os.listdir(path):
        if path.joinpath(folder).is_dir() and '__' not in folder:
            yield folder


def load_all_endpoints(path: Path):
    all_lambdas = get_all_lambdas_folder_name(path)
    for name_path in all_lambdas:
        if not path.joinpath(name_path).joinpath(configuration_name).exists():
            continue
        config = json.loads(path.joinpath(name_path).joinpath(configuration_name).read_text())
        swagger = config['swagger']
        endpoint = list(swagger)[0] if swagger else ''
        verbs = str(', ').join((list(swagger[endpoint]))) if swagger else ''
        yield endpoint, verbs, name_path


def delete_endpoint(*, lambda_name: str, path: Path):
    config_path = path.joinpath(lambda_name).joinpath(configuration_name)
    config = json.loads(config_path.read_text())
    config.update({'swagger': {}})
    config_path.write_text(json.dumps(config, indent=2))


def parse_api_verb_definition(*, name: str, swagger_definition: Dict):
    _api_verbs = json.dumps(swagger_definition)
    _api_verbs = _api_verbs.replace('{{lambdaName}}', name.replace('-', ' ').replace("_", " ").title().replace(" ", ""))
    return json.loads(_api_verbs)


def add_endpoint_to_lambda_existent(*, endpoint: str, verb: Verbs, cors: bool, lambda_name: str, path: Path):
    config_path = path.joinpath(lambda_name).joinpath(configuration_name)
    config = json.loads(config_path.read_text())
    swagger_configuration = create_swagger_configuration(lambda_name=lambda_name, endpoint=endpoint, verb=verb,
                                                         cors=cors)
    config.update({"swagger": swagger_configuration})

    config_path.write_text(json.dumps(config, indent=2))


def create_new_lambda_with_endpoint(*, lambda_name: str, handler: str, endpoint: str, verb: Verbs, cors: bool,
                                    path: Path):
    new_lambda_folder = path.joinpath(lambda_name)
    cfn_lambda = create_lambda_configuration(new_lambda_folder=new_lambda_folder, handler=handler, name=lambda_name)
    swagger_config = create_swagger_configuration(lambda_name=lambda_name, endpoint=endpoint, verb=verb, cors=cors)
    create_endpoint_configuration(new_lambda_folder=new_lambda_folder, swagger_configuration=swagger_config,
                                  cfn_configuration=cfn_lambda)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def rename_lambda(*, old_path, new_path):
    if not new_path.joinpath(configuration_name).exists():
        return None
    configuration = new_path.joinpath(configuration_name).read_text()
    configuration = configuration.replace(old_path.name, new_path.name)
    if json.loads(configuration).get('swagger'):
        old_reference_name = snake_case_or_kebab_case_to_pascal_case(old_path.name)
        new_reference_name = snake_case_or_kebab_case_to_pascal_case(new_path.name)
        configuration = configuration.replace(old_reference_name, new_reference_name)
    new_path.joinpath(configuration_name).write_text(configuration)


# ---------------------------------------------------------------------------------------------------------------------


def rename_endpoint(*, path: Path, new_endpoint: str):
    """
    Change the name of an endpoint
    :param path: actual path name
    :param new_endpoint: new path name
    :return:
    """
    config_path = path.joinpath(configuration_name)
    configuration = json.loads(config_path.read_text())
    path = list(configuration['swagger'])[0]
    definition = configuration['swagger'].pop(path)
    configuration['swagger'][new_endpoint] = definition
    config_path.write_text(json.dumps(configuration, indent=2))


def parse_lambda_code(handler: str):
    """
    Build the base code for any lambda in this project.

    :param handler:
    :return:
    """
    _path_lambda_template = Path(load_config().templates.code.lambda_template)
    code_lambda = _path_lambda_template.read_text()
    return code_lambda.format(handler=handler)


def parse_lambda_cfn_configuration(*, handler: str, name: str, path: Path):
    """
    Build a json with the lambda spec for cloud formation.
    :param handler:
    :param name:
    :param path:
    :return:
    """
    _path_lambda_cfn = Path(load_config().templates.code.lambda_cfn_template)
    cfn_lambda = json.loads(_path_lambda_cfn.read_text())
    cfn_lambda['Properties']['FunctionName'][FN_SUB] = cfn_lambda['Properties']['FunctionName'][FN_SUB].replace(
        "{{name}}", name)
    cfn_lambda['Properties']['Code'] = cfn_lambda['Properties']['Code'].replace("{{code}}",
                                                                                path.__str__().replace(os.sep, '/'))
    cfn_lambda['Properties']['Handler'] = cfn_lambda['Properties']['Handler'].replace("{{handler}}", handler)
    return cfn_lambda


def parse_lambda_swagger_configuration(*, verb: Verbs, lambda_name: str, endpoint: str, cors: bool):
    """

    :param verb:
    :param lambda_name:
    :param endpoint:
    :param cors:
    :return:
    """
    swagger_config = json.loads(path_lambda_swagger.read_text())
    verb_definition = swagger_config.pop('definition')
    verb_definition = parse_api_verb_definition(name=lambda_name, swagger_definition=verb_definition)
    configuration = {endpoint: {verb: verb_definition}}
    if cors:
        configuration[endpoint].update(swagger_config)
    return configuration


def validate_if_exist_verb_in_endpoint(verb: Verbs, endpoint: str):
    """
    Validation for verbs inside an endpoint.
    :param verb:
    :param endpoint:
    :return:
    """
    work_path = Path(load_config().project.folders.lambdas)
    endpoints = {}
    for lmd in os.listdir(work_path):
        if not work_path.joinpath(lmd).is_dir() or (not work_path.joinpath(lmd).joinpath(configuration_name).exists()):
            continue
        config = json.loads(work_path.joinpath(lmd).joinpath(configuration_name).read_text())
        swagger = config['swagger']
        original_endpoint = list(swagger)[0] if swagger else None
        if not original_endpoint:
            continue
        verbs = list(swagger[original_endpoint])
        endpoints.setdefault(original_endpoint, [])
        endpoints[original_endpoint] += verbs
    if verb in endpoints.get(endpoint, []):
        Debug.error(f"Already exist the verb: {verb} in the endpoint: {endpoint}")
        raise typer.Abort()


def add_new_layer_definition(name: str):
    """
    Add the cfn definition of a new layer inside the project.
    :return:
    """
    global_params = load_config()
    path = Path(global_params.templates.deploy.project_template)
    cfn_definition = json.loads(path.read_text())
    cfn_definition['Resources'][f'Layer{name.capitalize()}'] = {
        "Type": "AWS::Lambda::LayerVersion",
        "Properties": {
            "CompatibleRuntimes": [
                "python3.8",
                "python3.9"
            ],
            "Content": f"../{global_params.project.folders.layers}/{name}",
            "LayerName": {
                FN_SUB: "${Environment}-" + name
            }
        }
    }
    path.write_text(json.dumps(cfn_definition, indent=2))


def delete_layer_definition(name: str):
    """
    Delete an existent lambda in the cfn definition.
    :param name:
    :return:
    """
    global_params = load_config()
    path = Path(global_params.templates.deploy.project_template)
    cfn_definition = json.loads(path.read_text())
    try:
        del cfn_definition['Resources'][f'Layer{name.capitalize()}']
        path.write_text(json.dumps(cfn_definition, indent=2))
    except KeyError:
        Debug.error(f"The layer with the name {name} does not exsit")
        typer.Abort()


def rename_layer_definition(*, src: str, dst: str):
    """
    Rename the layer name in the cfn definition.
    :param src:
    :param dst:
    :return:
    """
    global_params = load_config()
    path = Path(global_params.templates.deploy.project_template)
    cfn_definition = json.loads(path.read_text())
    try:
        cfn_definition['Resources'].pop(f'Layer{src.capitalize()}')
        path.write_text(json.dumps(cfn_definition, indent=2))
        add_new_layer_definition(dst)
    except KeyError:
        Debug.error(f"The layer with the name {src} does not exsit")
        typer.Abort()
