from os import PathLike
from typing import Union

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
