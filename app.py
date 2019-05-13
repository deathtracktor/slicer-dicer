"""
    The Slicer/Dicer app.
"""
import asyncio
from asyncio import Queue
from pathlib import Path

import aiofiles
from aiofiles import os
from aiohttp import web

from lib.routes import routes
from lib import storage


DATA_PATH = str((Path(__file__).parent / 'data').resolve())


async def process_incoming(queue):
    """Process incoming files."""
    while True:
        file = await queue.get()
        relpath = await storage.put_file(file['tmp'])
        print(relpath)


async def start_background_tasks(app):
    """Schedule the necessary background tasks."""
    queue = app['incoming']
    loop = asyncio.get_running_loop()
    loop.create_task(process_incoming(queue))


def build_app():
    """Initialize the application and it's components."""
    app = web.Application()
    app['incoming'] = Queue()
    app.on_startup.append(start_background_tasks)
    app.add_routes(routes)
    storage.setup(DATA_PATH)
    return app


if __name__ == '__main__':
    web.run_app(build_app())
