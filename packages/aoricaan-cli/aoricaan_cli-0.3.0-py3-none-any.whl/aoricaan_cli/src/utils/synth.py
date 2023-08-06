import json
import os
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List

import tqdm
import typer
from dotenv import load_dotenv

from aoricaan_cli.src.utils.debugger import Debug
from aoricaan_cli.src.utils.str_parser import snake_case_or_kebab_case_to_pascal_case

try:
    from core_aws.s3 import upload_file
except ImportError:
    pass

environs = load_dotenv()


def _search_all_deploy_resources(template_data: Dict[str, Any]) -> List[str]:
    return [resource for resource in template_data["Resources"]
            if template_data["Resources"][resource].get("Type", {}) == "AWS::ApiGateway::Deployment"]


def update_deploy_resource_name(path_template: Path):
    template_text = path_template.read_text()
    deploys = _search_all_deploy_resources(json.loads(template_text))
    for deploy_key in deploys:
        Debug.info(f"Update deploy resource {deploy_key}")
        template_text = template_text.replace(f'"{deploy_key}"', f'"{deploy_key}{int(time.time())}"')
    path_template.write_text(template_text)


def update_deploy_id_resource_api_gateway(paths_template: List[Path]):
    for path_template in paths_template:
        update_deploy_resource_name(path_template)


def _create_layer_zip(*, layers_zips, layer, layer_path: Path, bucket):
    zip_path_file = os.path.join(layers_zips, f'{layer}.zip')
    with zipfile.ZipFile(zip_path_file, 'w') as my_zip:
        for _sub_dir in os.listdir(layer_path):
            sub_path = layer_path.joinpath(_sub_dir)
            for file in os.listdir(sub_path) if sub_path.is_dir() else []:
                my_zip.write(sub_path.joinpath(file), os.path.join('python', _sub_dir, file))
    if not upload_file(file_name=zip_path_file, bucket=bucket):
        print(f"Error to try save the layer zip in s3 {bucket}")


def build_layers(*, layers_path: Path, bucket=None, use_zip=False):
    layers_zips = 'layers_zips'
    if not os.path.exists(layers_zips):
        os.mkdir(layers_zips)

    for layer in tqdm.tqdm(os.listdir(layers_path)):
        layer_path = layers_path.joinpath(layer)
        if not layer_path.is_dir():
            continue

        layer_path = layer_path.joinpath('python')
        try:
            print('runing command', f'pip install -r {os.path.join(layer_path, "requirements.txt")} -t {layer_path}')
            os.system(f'pip install -r {os.path.join(layer_path, "requirements.txt")} -t {layer_path}')
        except Exception as e:
            print("WARNING: ", str(e))
        if use_zip:
            _create_layer_zip(layers_zips=layers_zips, layer=layer, layer_path=layer_path, bucket=bucket)


def read_templates_definition(paths: List[Path]):
    return {_path: json.loads(_path.read_text()) for _path in paths}


def write_templates_definition(templates_definition):
    [_template.write_text(json.dumps(_data)) for _template, _data in templates_definition.items()]


def _get_parents(*, lambda_configuration: Dict[str, Any], default: List[str], node: str = None):
    if node:
        _parents = lambda_configuration[node].pop("Parent", "")
    else:
        _parents = lambda_configuration.pop("Parent", "")

    if not isinstance(_parents, (str, list, tuple)):
        typer.Abort("Parent key data type error")

    if _parents and isinstance(_parents, str):
        return _parents.split(",")
    return _parents or default


def synth_endpoints(*, lambda_configuration: Dict[str, Any], path_swagger_template: List[Path],
                    swagger_templates: Dict[Path, Dict[str, Any]]):
    swagger_parents = _get_parents(node="swagger",
                                   lambda_configuration=lambda_configuration,
                                   default=[str(path_swagger_template[0])])

    for endpoint, endpoint_data in lambda_configuration['swagger'].items():

        endpoint_parents = _get_parents(lambda_configuration=endpoint_data,
                                        default=swagger_parents)

        for endpoint_parent in endpoint_parents:
            endpoint_parent = Path(endpoint_parent.strip())
            swagger_templates[Path(endpoint_parent)]['paths'].setdefault(endpoint, {})

            for endpoint_method in endpoint_data:
                if endpoint_method not in swagger_templates[endpoint_parent]['paths'][endpoint]:
                    swagger_templates[endpoint_parent]['paths'][endpoint].update(
                        {endpoint_method: endpoint_data[endpoint_method]})
                    continue
                Debug.warning(f"The path {endpoint} with method {endpoint_method} is duplicated.")
                if endpoint_method != "options":
                    raise typer.Abort()
                Debug.warning("These was override")


def build_all_lambdas(*,
                      lambdas_path: Path,
                      path_cfn_template: List[Path],
                      path_swagger_template: List[Path],
                      bucket=None):
    cfn_templates = read_templates_definition(path_cfn_template)
    swagger_templates = read_templates_definition(path_swagger_template)

    for configuration_path in lambdas_path.glob("*/configuration.json") or []:
        lambda_name = snake_case_or_kebab_case_to_pascal_case(configuration_path.parent.name)
        lambda_configuration = json.loads(configuration_path.read_text())

        cfn_parents = _get_parents(node="cfn",
                                   lambda_configuration=lambda_configuration,
                                   default=[str(path_cfn_template[0])])

        for cfn_parent in cfn_parents:
            cfn_templates[Path(cfn_parent.strip())]['Resources'][lambda_name] = lambda_configuration['cfn']

        synth_endpoints(lambda_configuration=lambda_configuration,
                        path_swagger_template=path_swagger_template,
                        swagger_templates=swagger_templates)

    write_templates_definition(cfn_templates)
    write_templates_definition(swagger_templates)

    # upload_file(file_name=path_swagger_template, bucket=bucket)
