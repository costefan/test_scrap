import os

from aiohttp import web
from aiohttp_swagger import setup_swagger
from .routes import app_routes

from .config.cache import BASE_DIR


def setup_routes(app: web.Application):
    for route in app_routes:
        app.router.add_route(*route)

    setup_swagger(app, swagger_from_file=os.path.join(
        BASE_DIR, 'docs/' 'swagger.yaml'))


def create_app(loop):
    app = web.Application(middlewares=[web.normalize_path_middleware()])

    app.update(name='games_scrapper')
    app.on_startup.append(setup_routes)

    return app
