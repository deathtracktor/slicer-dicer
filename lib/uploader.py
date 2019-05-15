"""
    File uploader routines.
"""
import hashlib
import os
from contextlib import suppress
from tempfile import NamedTemporaryFile

import aiofiles
import aiohttp


def get_tmpfile():
    """Return a unique temporary file name."""
    with NamedTemporaryFile(mode='a', delete=False) as tmpfile:
        return tmpfile.name

        
async def handle_file(field):
    """Handle a binary file."""
    tmpfile = get_tmpfile()
    async with aiofiles.open(tmpfile, mode='wb') as f:
        hash = hashlib.sha256()
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            hash.update(chunk)
            await f.write(chunk)
    return {
        'tmp': tmpfile,
        'sha256': hash.hexdigest(),
        'ext': os.path.splitext(field.filename)[1],
    }

    
async def send_head(url):
    """Send a preflight check request."""
    with suppress(aiohttp.ClientConnectorError):
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as resp:
                return resp.status == 200

                
async def handle_callback_url(field):
    """Handle and validate the callback URL."""
    raw = await field.read()
    url = raw.decode('utf-8')
    if not await send_head(url):
        raise NameError('Callback URL "{}" is not reachable.'.format(url))
    return {'callback_url': url}


async def parse_request(request):
    """Extract fields from a multi-part request."""
    reader = await request.multipart()
    res = []
    handlers = {
        'file': handle_file,
        'callback_url': handle_callback_url,
    }
    field_names = handlers.keys()
    while True:
        field = await reader.next()
        if not field:
            break
        handler = handlers.pop(field.name, None)
        if not handler:
            raise NameError((
                'Invalid/redundand field name "{}". '
                'Valid names are {}.'
            ).format(field.name, ', '.join(field_names)))
        yield await handler(field)
    if handlers:
        err = 'Missing required field(s): {}'.format(', '.join(handlers.keys()))
        raise NameError(err)
