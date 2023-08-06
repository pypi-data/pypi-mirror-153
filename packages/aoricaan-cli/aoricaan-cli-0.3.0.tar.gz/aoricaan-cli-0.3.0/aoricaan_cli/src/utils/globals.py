import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar, Type, cast, Callable, List

import toml
from dotenv import load_dotenv

from aoricaan_cli.src.utils.debugger import Debug

T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_str_to_list(x: Any) -> List[str]:
    assert isinstance(x, str)
    return [x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Definition:
    name: str
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'Definition':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        return Definition(name, description)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "description": from_str(self.description)}
        return result


@dataclass
class Folders:
    lambdas: str
    layers: str

    @staticmethod
    def from_dict(obj: Any) -> 'Folders':
        assert isinstance(obj, dict)
        lambdas = from_str(obj.get("lambdas"))
        layers = from_str(obj.get("layers"))
        return Folders(lambdas, layers)

    def to_dict(self) -> dict:
        result: dict = {"lambdas": from_str(self.lambdas), "layers": from_str(self.layers)}
        return result


@dataclass
class Project:
    definition: Definition
    folders: Folders

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        definition = Definition.from_dict(obj.get("definition"))
        folders = Folders.from_dict(obj.get("folders"))
        return Project(definition, folders)

    def to_dict(self) -> dict:
        result: dict = {"definition": to_class(Definition, self.definition), "folders": to_class(Folders, self.folders)}
        return result


@dataclass
class Code:
    lambda_template: str
    lambda_cfn_template: str
    swagger_template: str

    @staticmethod
    def from_dict(obj: Any) -> 'Code':
        assert isinstance(obj, dict)
        lambda_template = from_str(obj.get("lambda_template"))
        lambda_cfn_template = from_str(obj.get("lambda_cfn_template"))
        swagger_template = from_str(obj.get("swagger_template"))
        return Code(lambda_template, lambda_cfn_template, swagger_template)

    def to_dict(self) -> dict:
        result: dict = {"lambda_template": from_str(self.lambda_template),
                        "lambda_cfn_template": from_str(self.lambda_cfn_template),
                        "swagger_template": from_str(self.swagger_template)}
        return result


@dataclass
class Deploy:
    project_template: str
    api_swagger_template: str

    @staticmethod
    def from_dict(obj: Any) -> 'Deploy':
        assert isinstance(obj, dict)
        project_template = from_union([lambda x: from_list(from_str, x), from_str_to_list], obj.get("project_template"))
        api_swagger_template = from_union([lambda x: from_list(from_str, x), from_str_to_list],
                                          obj.get("api_swagger_template"))
        return Deploy(project_template, api_swagger_template)

    def to_dict(self) -> dict:
        result: dict = {"project_template": from_str(self.project_template),
                        "api_swagger_template": from_str(self.api_swagger_template)}
        return result


@dataclass
class Templates:
    code: Code
    deploy: Deploy

    @staticmethod
    def from_dict(obj: Any) -> 'Templates':
        assert isinstance(obj, dict)
        code = Code.from_dict(obj.get("code"))
        deploy = Deploy.from_dict(obj.get("deploy"))
        return Templates(code, deploy)

    def to_dict(self) -> dict:
        result: dict = {"code": to_class(Code, self.code), "deploy": to_class(Deploy, self.deploy)}
        return result


@dataclass
class Config:
    project: Project
    templates: Templates

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        project = Project.from_dict(obj.get("project"))
        templates = Templates.from_dict(obj.get("templates"))
        return Config(project, templates)

    def to_dict(self) -> dict:
        result: dict = {"project": to_class(Project, self.project), "templates": to_class(Templates, self.templates)}
        return result


def config_from_dict(s: Any) -> Config:
    return Config.from_dict(s)


def config_to_dict(x: Config) -> Any:
    return to_class(Config, x)


def load_config(path="apm_project.toml") -> Config:
    config_path = Path(path)
    if not config_path.exists():
        Debug.warning("config file not found in the project.")
        load_dotenv(".env")
        app_name = os.getenv("app_name") or ""
        config_path.write_text(f"""[apm.project.definition]
name = "{app_name}"
description = ""

[apm.templates.code]
lambda_template = "utils/templates/lambda.txt"
lambda_cfn_template = "utils/templates/lambda.json"
swagger_template = "utils/templates/api_verbs.json"

[apm.templates.deploy]
project_template = "templates/projectTemplate.json"
api_swagger_template = "src/api.json"

[apm.project.folders]
lambdas = "src/lambdas"
layers = "src/layers"
        """)
        Debug.info(
            f"Created config file at {config_path} in this path you can find all configuration for the project here.")
        Debug.warning(f"Please add the file {config_path} to git tracking and commit it")
    toml_config = toml.loads(config_path.read_text())
    return config_from_dict(toml_config["apm"])
