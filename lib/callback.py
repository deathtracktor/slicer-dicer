"""
    Send success notifications back to the requesting service.
"""
import asyncio
import os
import logging
from urllib.parse import urljoin

import aiohttp


BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1/')
CALLBACK_RETRIES = (10, 120, 600,)


async def send(callback_url, relpath, sha256, retries=iter(CALLBACK_RETRIES), **_):
    """Send a notification back to the requesting service."""
    payload = {
        'url': urljoin(BASE_URL, relpath),
        'sha256': sha256,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(callback_url, data=payload) as resp:
                assert resp.status == 200, 'HTTP {}'.format(resp.status)
                logging.info('Callback for file "%s" sent to "%s".', relpath, callback_url)
    except Exception as exc:
        delay = next(retries, False)
        if delay is False:
            logging.critical('Callback "%s" failed, giving up.', callback_url)
        logging.info(
            'Callback "%s" failed: "%s", will retry in %ds...',
            callback_url, exc, delay
        )
        await asyncio.sleep(delay)
        loop = asyncio.get_running_loop()
        loop.create_task(send(callback_url, relpath, sha256, retries))
