import re
import bs4

from app.exceptions import ParsingError


class Scrapper:

    def __init__(self, url: str):
        self.url = url

    async def get_page_content(self, session):
        """Get page content and parse with bs
        :param session:
        :return: 
        """

        async def parse_page():
            async with session.get(self.url) as response:
                page = await response.text()

            return self.__read_page(page)

        parsed_fields = await parse_page()

        return parsed_fields

    def __read_page(self, page):
        """Parse with beautifulSoup"""
        soup = bs4.BeautifulSoup(page, 'html.parser')
        try:
            game_panels = soup.select(
                'div.id-cluster-container.cluster-container'
                '.cards-transition-enabled')

            games = []
            # Go through categories panels
            for panel in game_panels:
                category = panel.select_one(
                    'h2.single-title-link a').get_text()

                for game_card in panel.select('div.card'):
                    game_name = game_card.select_one(
                        'div.card-content div.details a.title'
                    ).get_text().strip()
                    games.append({'category': category, 'name': game_name})

        except Exception:
            raise ParsingError("Parsing error, api has changed or smth...")

        return {
            'url': page,
            'games': games
        }
