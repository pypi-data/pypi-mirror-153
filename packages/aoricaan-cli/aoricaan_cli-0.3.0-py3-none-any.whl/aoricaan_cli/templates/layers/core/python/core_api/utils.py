import json

__all__ = [
    "get_body"
]


def get_body(event: dict):
    """
    get event body if lambda has proxy lambda integration in api_local gateway
    Args:
        event: The event received from the invocation via api_local gateway

    Returns: the value for the body if this exist else None

    """
    if isinstance(event, str):
        event = json.loads(event)
    body = event.get('body')
    if isinstance(body, str):
        return json.loads(body)
    return body


def get_status_code(response):
    """
    Get a status code from the lambda response if you use the decorator LambdaResponseWebDefault
    Args:
        response: Lambda response

    Returns: A status code if exist

    """
    status_code = response.get('statusCode')
    return status_code
