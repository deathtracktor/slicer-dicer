"""
    The Slicer/Dicer app.
"""
import asyncio
from asyncio import Queue

import logging
import os
import sys

from collections import ChainMap
from contextlib import suppress
from pathlib import Path

from aiohttp import web

DATA_PATH = str((Path(__file__).parent / 'data').resolve())

from lib.routes import routes
from lib import callback, storage


async def process_incoming(incoming, processed):
    """Persist incoming files in the HashFS."""
    with suppress(asyncio.CancelledError):
        while True:
            file = await incoming.get()
            relpath = await storage.put_file(file['tmp'], file['ext'])
            await processed.put(ChainMap(file, {'relpath': relpath}))
            logging.info('"%(sha256)s" added to storage.', file)
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, os.remove, file['tmp'])
            await asyncio.sleep(1)


async def send_callback(queue):
    """Send a success callback."""
    with suppress(asyncio.CancelledError):
        while True:
            file = await queue.get()
            await callback.send(**file)


async def start_background_tasks(app):
    """Schedule the necessary background tasks."""
    loop = asyncio.get_running_loop()
    loop.create_task(process_incoming(app['incoming'], app['processed']))
    loop.create_task(send_callback(app['processed']))


def build_app():
    """Initialize the application and it's components."""
    app = web.Application()
    app['incoming'], app['processed'] = Queue(), Queue()
    app.on_startup.append(start_background_tasks)
    app.add_routes(routes)
    storage.setup(DATA_PATH)
    return app


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    web.run_app(build_app())
