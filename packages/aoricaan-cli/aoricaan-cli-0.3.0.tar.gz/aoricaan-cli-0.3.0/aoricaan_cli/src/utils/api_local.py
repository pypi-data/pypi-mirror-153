import json
import os
import shutil
import uuid
from pathlib import Path

__all__ = [
    'read_all_lambdas',
    'build_and_run',
    'read_swagger_template',
    'build_files_for_api_local'
]

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast, Dict, Optional, List

from aoricaan_cli.src.utils.globals import load_config

T = TypeVar("T")
optional_str = 'Optional[{code}]'

router_path = Path('src/api_local/router.py')


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int)
    return x


def from_dict(x: Any) -> Dict[str, Any]:
    assert isinstance(x, dict)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs: List[Any], x: Any):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class CustomString:
    def __init__(self, value, family=None):
        self.value = value
        self.family = family

    def __add__(self, other):
        if not isinstance(other, CustomString) or other.family != self.family:
            raise ValueError('Only same type or family can be added')
        if self.value and other.value:
            result = f'{self.value}, {other.value}'
        elif self.value and not other.value:
            return self
        elif not self.value and other.value:
            return other
        else:
            result = ''
        return CustomString(result, self.family)

    def __str__(self):
        return self.value


@dataclass
class Parameter:
    name: str
    parameter_in: str
    required: bool
    parameter_type: str
    enum: Optional[List[str]]
    default: Optional[Any]
    minimum: Optional[Any]
    maximum: Optional[Any]
    description: Optional[Any]
    min_items: Optional[Any]
    max_items: Optional[Any]
    unique_items: Optional[Any]
    items: Optional[Any]
    schema: Optional[Any]
    __data_types = {
        "integer": "int",
        "string": "str",
        "boolean": "bool"
    }

    @staticmethod
    def from_dict(obj: Any) -> 'Parameter':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        parameter_in = from_str(obj.get("in"))
        required = from_bool(obj.get("required"))
        parameter_type = from_str(obj.get("type"))
        enum = obj.get("enum")
        default = from_union([from_int, from_str, from_none], obj.get("default"))
        minimum = from_union([from_int, from_str, from_none], obj.get("minimum"))
        maximum = from_union([from_int, from_str, from_none], obj.get("maximum"))
        description = from_union([from_int, from_str, from_none], obj.get("description"))
        min_items = from_union([from_int, from_str, from_none], obj.get("minItems"))
        max_items = from_union([from_int, from_str, from_none], obj.get("maxItems"))
        unique_items = from_union([from_int, from_str, from_none], obj.get("uniqueItems"))
        items = from_union([from_int, from_str, from_none], obj.get("items"))
        schema = from_union([from_dict, from_none], obj.get("schema"))
        return Parameter(name, parameter_in, required, parameter_type, enum,
                         default, minimum, maximum, description, min_items,
                         max_items, unique_items, items, schema)

    def synth(self):
        return getattr(self, self.parameter_in)()

    def header(self):
        code = f'{self.name.replace("-", "_")}: {self.__data_types.get(self.parameter_type, "str")} = '
        code += 'Header(...)' if self.required else 'Header(None)'
        code = CustomString(code, 'param_header')
        headers = CustomString(f'"{self.name}": {self.name.replace("-", "_")}', 'dict_header')
        return code, headers

    def query(self):
        code = f'{self.name.replace("-", "_")}: {self.__data_types.get(self.parameter_type, "str")} = '
        code += f'Query(...)' if self.required else f'Query(None)'
        code = CustomString(code, 'param_query')
        query_params = CustomString(f'"{self.name}": {self.name.replace("-", "_")}', 'dict_query')
        return code, query_params

    def path(self):
        code = f'{self.name.replace("-", "_")}: {self.__data_types.get(self.parameter_type, "str")}'
        code = CustomString(code, 'param_path')
        path_params = CustomString(f'"{self.name}": {self.name.replace("-", "_")}', 'dict_path')
        return code, path_params

    def body(self):
        if not self.schema:
            code = CustomString('payload: dict = Body(None)', 'body_param')
            payload = CustomString('"body": json.dumps(payload)', 'dict_body')
            model = None
        else:
            if self.schema.get("type") != "object":
                raise ValueError("Only object type is supported for body")
            _model_name = f"{self.name.capitalize()}{uuid.uuid4().hex}"
            code = CustomString(f'payload: {_model_name}', 'body_param')
            payload = CustomString('"body": json.dumps(payload.dict())', 'dict_body')
            model = self.__build_model(_model_name)
        return (code, model), payload

    def __build_model(self, model_name):
        _model = f"class {model_name}(BaseModel):\n"
        properties = self.schema.get("properties")
        for _property in properties:
            _data_type = self.__data_types.get(properties[_property].get("type"), "str")
            _data_type = f"Optional[{_data_type}] = None" if _property not in self.schema.get("required",
                                                                                              []) else _data_type
            _model += f'\t{_property}: {_data_type}\n'
        return _model


def parameter_from_dict(s: Any) -> Parameter:
    return Parameter.from_dict(s)


class EndpointConfiguration:
    def __init__(self, *, path: str, method: str, name: str, parameters, handler: str):
        self.__name = name
        self.__handler = handler
        self.__path = path
        self.__method = method
        self.__parameters = parameters
        self.__data_types = {
            "integer": "int",
            "string": "str",
            "boolean": "bool"
        }

    def synth(self):
        params, event_code, model = self.build_params()
        code = f'''{model}\n\n@router.{self.__method.lower()}("{self.__path}")\nasync def {self.__name}(response: Response, {params}):\n\t{event_code}\n\tres = {self.__handler}(event, None)\n\tresponse.status_code = get_status_code(res)\n\treturn get_body(res)\n\n'''
        return code

    def build_params(self):
        params = {}
        params_code = {}
        model = None
        for param in self.__parameters:
            parameter_instance = parameter_from_dict(param)
            result = parameter_instance.synth()
            if not result:
                continue
            code, d = result
            try:
                code, model = code
            except TypeError:
                pass
            if parameter_instance.parameter_in not in params:
                params.setdefault(parameter_instance.parameter_in, code)
                params_code.setdefault(parameter_instance.parameter_in, d)
            else:
                params.update({parameter_instance.parameter_in: params[parameter_instance.parameter_in] + code})
                params_code.update({parameter_instance.parameter_in: params_code[parameter_instance.parameter_in] + d})
        parameters = dict(map(lambda x: (str(x[0]), str(x[1])), params.items()))
        event_dict = dict(map(lambda x: (str(x[0]), str(x[1])), params_code.items()))
        parameters_result = (CustomString(parameters.get("path")) +
                             CustomString(parameters.get("query")) +
                             CustomString(parameters.get("body")) +
                             CustomString(parameters.get("header"))
                             )

        headers = CustomString(event_dict.get('header'))
        query_string_parameters = CustomString(event_dict.get('query'))
        path_parameters = CustomString(event_dict.get('path'))

        headers = CustomString("'headers':" + "{" + f"{headers}" + "}" if headers.value else "")
        query_string_parameters = CustomString(
            "'queryStringParameters':" + "{" + f"{query_string_parameters}" + "}" if query_string_parameters.value else "")
        path_parameters = CustomString(
            "'pathParameters':" + "{" + f"{path_parameters}" + "}" if path_parameters.value else "")

        event_result = ("event = {" +
                        str(headers +
                            query_string_parameters +
                            path_parameters +
                            CustomString(event_dict.get('body'))) + "}")
        return parameters_result, event_result, model


def read_swagger_template(path):
    with open(path, 'r') as f:
        swagger_template = json.load(f)
    return swagger_template


def read_configuration(path):
    try:
        with open(os.path.join(path, 'configuration.json'), 'r') as f:
            configuration = json.load(f)
    except FileNotFoundError:
        return {}
    return configuration


def process_api_paths(*, lambda_configuration, handler):
    if not lambda_configuration:
        return None

    all_endpoints = ''
    for path, v in lambda_configuration['swagger'].items():
        method = list(filter(lambda x: x != 'options', v))[0]
        lambda_name = v[method]['x-amazon-apigateway-integration']['uri']['Fn::Join'][1][1]['Fn::GetAtt'][0]
        endpoint = EndpointConfiguration(path=path, method=method, name=lambda_name, parameters=v[method]['parameters'],
                                         handler=handler)
        all_endpoints += endpoint.synth()

    return all_endpoints


def read_all_lambdas(*, lambdas_path, swagger_template):
    all_imports = 'from fastapi import APIRouter\nfrom fastapi import Body, Header, Query, Response\nfrom core_api.utils import get_body, get_status_code\nimport json\nfrom pydantic import BaseModel\nfrom typing import Optional\n'
    all_endpoints = 'router = APIRouter()\n\n'

    for name in os.listdir(lambdas_path):
        path = os.path.join(lambdas_path, name)
        if (path == lambdas_path) or not (os.path.isdir(path)):
            continue

        configuration = read_configuration(path)
        name_handler = f'{name}_handler'
        endpoint = process_api_paths(lambda_configuration=configuration, handler=name_handler)
        if endpoint:
            all_endpoints += endpoint
            all_imports += f'from src.lambdas.{name}.lambda_function import lambda_handler as {name}_handler\n'

    with open('src/api_local/router.py', 'w') as f:
        f.write(all_imports)
        f.write('\n\n')
        f.write(all_endpoints)


def build_files_for_api_local(*, reload=False):
    configuration = load_config()
    if reload and not Path('src/api_local').exists():
        return None
    swagger_data = read_swagger_template(configuration.templates.deploy.api_swagger_template)
    read_all_lambdas(lambdas_path=configuration.project.folders.lambdas, swagger_template=swagger_data)


def build_and_run():
    api_local = os.path.join(os.getcwd(), 'src', 'api_local')
    if not os.path.exists(api_local):
        os.mkdir(api_local)
    with open(os.path.join(api_local, 'app.py'), 'w') as f:
        f.write('''
from fastapi import FastAPI
from mangum import Mangum
from src.api_local.router import router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


load_dotenv()

env = os.getenv('ENVIRONMENT', None)


app = FastAPI(title='Test API',
              description='API ')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=f"/{env.lower() or 'v1'}")


@app.get("/")
def read_root():
    return {"Message": "Api deployed with aoricaan-src"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
''')
    build_files_for_api_local()
    try:
        os.system('uvicorn src.api_local.app:app --port=3000 --reload')
    except KeyboardInterrupt as e:
        shutil.rmtree("src/api_local")
        raise e
