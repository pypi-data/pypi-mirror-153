import json
import os

with open("utils/templates/api_verbs.json") as f:
    api_verbs = json.load(f)

with open("utils/templates/lambda.json") as f:
    cfn_lambda = json.load(f)

with open("utils/templates/lambda.txt") as f:
    code_lambda = f.read()


def get_api_verb_definition(*, name: str):
    _api_verbs = json.dumps(api_verbs['definition'])
    _api_verbs = _api_verbs.replace('{{lambdaName}}', name)
    return json.loads(_api_verbs)


def get_cnf_definitions(*, name: str, code: str, handler: str):
    _cfn_lambda = cfn_lambda
    _cfn_lambda['Properties']['FunctionName']["Fn::Sub"] = "${Environment}-" + name
    _cfn_lambda['Properties']['Code'] = code
    _cfn_lambda['Properties']['Handler'] = handler if handler else 'lambda_function.lambda_handler'
    return _cfn_lambda


def new_lambda(*, name, handler=None, method=None, path=None, cors=False):
    new_lambda_folder = f'src/lambdas/{name}'

    if os.path.exists(new_lambda_folder):
        raise LambdaAlreadyExist(name)

    verbs = ['get', 'post', 'put', 'patch', 'delete']
    api_definition = {"swagger": {path: {}}}
    if method and isinstance(method, (list, tuple)):
        for m in method:
            assert m in verbs
            api_definition['swagger'][path][m] = get_api_verb_definition(name=name)
    elif method and isinstance(method, str):
        api_definition['swagger'][path][method] = get_api_verb_definition(name=name)

    if api_definition['swagger'] and cors:
        api_definition['swagger'][path]['options'] = api_verbs['options']

    if not api_definition['swagger'][path]:
        api_definition = {}

    configurations = api_definition | {
        "cfn": get_cnf_definitions(name=name, code=new_lambda_folder, handler=handler)}

    os.mkdir(new_lambda_folder)

    with open(os.path.join(new_lambda_folder, 'lambda_function.py'), 'w') as f:
        f.write(code_lambda)

    with open(os.path.join(new_lambda_folder, '../../utils/__init__.py'), 'w') as f:
        f.write("")

    with open(os.path.join(new_lambda_folder, 'test_lambda_function.py'), 'w') as f:
        f.write("")

    with open(os.path.join(new_lambda_folder, 'configuration.json'), 'w') as f:
        f.write(json.dumps(configurations, indent=2))


class LambdaAlreadyExist(Exception):
    def __init__(self, name):
        super(LambdaAlreadyExist, self).__init__(f"\nERROR: The lambda with the name -> {name} <- already exist.")
