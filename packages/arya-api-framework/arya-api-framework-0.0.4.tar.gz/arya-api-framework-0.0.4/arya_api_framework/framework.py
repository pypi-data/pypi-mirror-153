from typing import Any

from .errors import MISSING


class ClientInit(type):
    def __call__(cls, *args, **kwargs) -> Any:
        uri = kwargs.get('uri', MISSING)
        if uri is MISSING and len(args) > 0:
            uri = args[0]
        headers = kwargs.get('headers', MISSING)
        cookies = kwargs.get('cookies', MISSING)
        parameters = kwargs.get('parameters', MISSING)
        error_responses = kwargs.get('error_responses', MISSING)
        bearer_token = kwargs.get('bearer_token', MISSING)

        obj = type.__call__(cls, uri=uri, headers=headers, cookies=cookies, parameters=parameters,
                            error_responses=error_responses, bearer_token=bearer_token)
        if hasattr(obj, '__post_init__'):
            obj.__post_init__(*args, **kwargs)
        return obj
