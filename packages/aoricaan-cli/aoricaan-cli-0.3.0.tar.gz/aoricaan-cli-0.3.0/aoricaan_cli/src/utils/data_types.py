from enum import Enum

import typer
from pydantic import BaseModel


class Verbs(str, Enum):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    PATCH = 'patch'
    DELETE = 'delete'


class Endpoint(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validator

    @classmethod
    def validator(cls, value):
        if not isinstance(value, str):
            raise ValueError("Value should be a string")
        if value[0] != '/':
            raise ValueError("An endpoint should be start with an slash like '/endpoint' ")
        return cls(value)


class LambdaName(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validator

    @classmethod
    def validator(cls, v):
        return cls(v)


class LambdaHandler(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validator

    @classmethod
    def validator(cls, v):
        return cls(v)


def endpoint_name_validation(endpoint: str):
    if endpoint and endpoint[0] != '/':
        raise typer.BadParameter('The enpoint should be start with a slash like, "/users"')
    elif not endpoint:
        raise typer.BadParameter('The endpoint don´t should be empty or None')
    else:
        return endpoint
