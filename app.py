"""
    The Slicer/Dicer app.
"""
from aiohttp import web

from lib.routes import routes

app = web.Application()
app.add_routes(routes)
web.run_app(app)