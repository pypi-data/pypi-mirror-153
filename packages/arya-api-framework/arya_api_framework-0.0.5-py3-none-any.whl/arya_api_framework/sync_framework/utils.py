from os import PathLike
from typing import Union


def chunk_file_reader(file: Union[str, PathLike[str]]):
    with open(file, 'rb') as f:
        chunk = f.read(64 * 1024)

        while chunk:
            yield chunk
            chunk = f.read(64 * 1024)
