import os.path

import aiohttp
from aiohttp import web

from .cacher import Cacher
from .exceptions import ParsingError, DataNotScrappedError
from .scrapper import Scrapper
from .config.response import JSON_DICT_OUTPUT
from .config.cache import CACHE_FILE


cacher = Cacher()


async def start_scrapping(request: web.Request) -> web.Response:
    try:
        body = await request.json()
        url = body['url']
        scrapper = Scrapper(url)

        async with aiohttp.ClientSession(loop=request.app.loop) as session:
            res = await scrapper.get_page_content(session)

        await cacher.save(res)
    except ParsingError as err:
        return web.json_response(
            {'errors': str(err)}, status=400
        )

    if JSON_DICT_OUTPUT:
        data = res['games']
    else:
        data = ["APP/{}/{}".format(game['category'], game['name'])
                for game in res['games']]

    return web.json_response(
        {'data': data,
         'count': len(res['games'])},
        status=200
    )

async def search_games(request: web.Request) -> web.Response:
    filters = request.query.get('search')
    try:
        res = await cacher.get(filters)
    except DataNotScrappedError:
        return web.json_response(
            {'error': 'Data not scrapped.'},
            status=404
        )

    return web.json_response(
        {'data': res},
        status=200
    )

async def export_games(_: web.Request):
    if not os.path.exists(CACHE_FILE):
        return web.json_response(
            {'error': 'Data not scrapped.'},
            status=404
        )

    return web.FileResponse(CACHE_FILE)
