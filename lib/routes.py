"""
    App routes.
"""
from aiohttp import web

from lib import uploader

routes = web.RouteTableDef()


@routes.post('/upload')
async def upload_file(request):
    """Upload an image file and optional metadata into a temporary folder."""
    fields = ('image', 'meta',)
    async for field, path in uploader.extract(request, fields):
        print(field, path)

    return web.Response()