import asyncio
from aiohttp import web

from app.main import create_app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    app = create_app(loop)
    web.run_app(app, port=8000)
