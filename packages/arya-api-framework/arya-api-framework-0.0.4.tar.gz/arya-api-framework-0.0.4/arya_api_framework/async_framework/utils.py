from os import PathLike
from typing import Union, Optional, Dict, Mapping, List
from collections import OrderedDict

from ..errors import AsyncClientError

is_async: bool
try:
    import aiofiles
    is_async = True
except ImportError:
    is_async = False


async def chunk_file_reader(file: Union[str, PathLike[str]]):
    if not is_async:
        raise AsyncClientError("The async context is unavailable. Try installing with `python -m pip install arya-api-framework[async]`.")

    async with aiofiles.open(file, 'rb') as f:
        chunk = await f.read(64 * 1024)

        while chunk:
            yield chunk
            chunk = await f.read(64 * 1024)


def _to_key_val_list(obj: Optional[Dict]) -> Optional[List]:
    if obj is None:
        return obj

    if isinstance(obj, (str, bytes, bool, int)):
        raise ValueError("Cannot encode objects that are not key-val paired.")

    if isinstance(obj, Mapping):
        obj = obj.items()

    return list(obj)


def merge_params(static_params: Optional[Dict], request_params: Optional[Dict]) -> Optional[Mapping]:
    if request_params is None:
        return static_params

    if static_params is None:
        return request_params

    if not (isinstance(static_params, Mapping) and isinstance(request_params, Mapping)):
        return request_params

    merged = OrderedDict(_to_key_val_list(static_params))
    merged.update(_to_key_val_list(request_params))

    none_keys = [k for (k, v) in merged.items() if v is None]
    for k in none_keys:
        del merged[k]

    return merged
