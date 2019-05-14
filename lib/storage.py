"""
    File system storage.
"""
import asyncio
from functools import partial

from hashfs import HashFS


async def put_file(fs, path, ext):
    """Copy a disk file into the storage, return it's new address."""
    loop = asyncio.get_running_loop()
    addr = await loop.run_in_executor(None, fs.put, path, ext)
    return addr.relpath


def setup(root_path):
    """Module initialization."""
    fs = HashFS(root_path, depth=3, width=2, algorithm='sha256')
    global put_file
    put_file = partial(getattr(put_file, 'func', put_file), fs)
