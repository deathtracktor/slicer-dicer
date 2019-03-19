"""
    The Slicer/Dicer app.
"""
from asyncio import Queue
from aiohttp import web

from lib.routes import routes


async def process_incoming(queue):
    """Process incoming files."""
    while True:
        file = await queue.get()
        print(file)


async def start_background_tasks(app):
    """Schedule the necessary background tasks."""
    queue = app['incoming']
    app.loop.create_task(process_incoming(queue))


app = web.Application()

app['incoming'] = Queue(loop=app.loop)
app.on_startup.append(start_background_tasks)
app.add_routes(routes)

web.run_app(app)