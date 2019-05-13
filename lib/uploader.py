"""
    File uploader routines.
"""
import hashlib
from tempfile import NamedTemporaryFile

import aiofiles
import aiohttp


async def handle_image(field):
    """Handle an image file."""
    with NamedTemporaryFile(mode='a', delete=False) as tmpfile:
        pass
    async with aiofiles.open(tmpfile.name, mode='wb') as f:
        hash = hashlib.sha256()
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            hash.update(chunk)
            await f.write(chunk)
    return {'tmp': tmpfile.name, 'sha256': hash.hexdigest()}


async def handle_callback_url(field):
    """Handle and validate the callback URL."""
    raw = await field.read()
    url = raw.decode('utf-8')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as resp:
                if resp.status != 200:
                    err = 'Unexpected callback response HTTP {}.'.format(resp.status)
                    raise NameError(err)
    except aiohttp.ClientConnectorError as exc:
        raise NameError('Callback URL is not reachable: "{}".'.format(exc))
    return {'callback_url': url}


async def parse_request(request):
    """Extract fields from a multi-part request."""
    reader = await request.multipart()
    res = []
    handlers = {
        'image': handle_image,
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
