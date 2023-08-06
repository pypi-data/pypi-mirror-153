import json
from core_utils.utils import cast_default


__all__ = [
    "api_response"
]

def api_response(body, status_code):
    try:
        body = json.dumps(body, default=cast_default, ensure_ascii=False)
    except Exception as details:
        print(str(details))
        raise details
    else:
        response = {"statusCode": status_code,
                    "body": body,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    }
        return response
