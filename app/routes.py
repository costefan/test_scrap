from .views import (
    start_scrapping, export_games, search_games
)


app_routes = [
    ('POST', '/scrap', start_scrapping),
    ('GET', '/export/', export_games),
    ('GET', '/', search_games)
]
