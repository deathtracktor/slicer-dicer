"""
    App routes.
"""
from aiohttp import web

from lib import uploader

routes = web.RouteTableDef()

@routes.post('/upload')
async def upload_file(request):
    """Upload an image file and optional metadata into a temporary folder."""
    queue = request.app['incoming']
    files = uploader.extract(request, ('image', 'meta',))
    queue.put_nowait([f async for f in files])
    return web.Response()
    