"""
    File uploader routines.
"""
from collections import namedtuple
from tempfile import NamedTemporaryFile

import aiofiles
import hashlib
from aiohttp import MultipartReader

File = namedtuple('File', ['type', 'hash', 'path'])


async def save_binary_file(field):
    """Upload a binary file, return temporary file name."""
    with NamedTemporaryFile(mode='w+b', prefix=field.name + '_', delete=False) as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    return f.name


async def get_file_hash(fpath):
    """Create output folders based on file's MD5 digest."""
    chunk_size = 1024 << 1
    md5 = hashlib.md5()
    async with aiofiles.open(fpath, mode='rb') as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()


async def extract(request, fields):
    """Extract fields from a multi-part request."""
    reader = await request.multipart()
    while True:
        field = await reader.next()
        if not field:
            break
        if field.name in fields:
            path = await save_binary_file(field)
            digest = await get_file_hash(path)
            yield File(field.name, digest, path)
