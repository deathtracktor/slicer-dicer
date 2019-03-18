"""
    File uploader routines.
"""
from tempfile import NamedTemporaryFile
from aiohttp import MultipartReader


async def extract(request, fields):
    """Extract fields from a multi-part request."""
    reader = await request.multipart()
    while True:
        field = await reader.next()
        if not field:
            break
        if field.name in fields:
            path = await save_binary_file(field)
            yield field.name, path


async def save_binary_file(field):
    """Upload a binary file, return temporary file name."""
    with NamedTemporaryFile(mode='w+b', prefix=field.name + '_', delete=False) as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    return f.name
