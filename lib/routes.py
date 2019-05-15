"""
    App routes.
"""
from collections import ChainMap
from aiohttp import web
from lib import uploader

routes = web.RouteTableDef()

# This route is for development only!
# In production, static content should be served
# directly by a web server.
from app import DATA_PATH
routes.static('/', DATA_PATH)

@routes.post('/upload')
async def upload_file(request):
    """Upload an image file and optional metadata into a temporary folder."""
    try:
        data = ChainMap(*[p async for p in uploader.parse_request(request)])
    except (NameError, KeyError) as exc:
        return web.HTTPBadRequest(reason=str(exc))
    await request.app['incoming'].put(dict(data))
    return web.HTTPOk(text='sha256:{sha256}'.format(**data))
