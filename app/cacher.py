import os.path
import pandas as pd

from .config.cache import CACHE_FILE
from .exceptions import DataNotScrappedError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class Cacher(metaclass=Singleton):

    def ___cache_data(self, games):
        df = pd.DataFrame(games, columns=['category', 'name'])
        df.to_csv(CACHE_FILE)

    async def save(self, res: dict):
        """Save data with games to file
        :param res: 
        :return: 
        """
        self.___cache_data(res['games'])

    def __get_data(self, filters):
        """Get data from cached file and filter it
        :param filter: 
        :return: 
        """
        if not os.path.exists(CACHE_FILE):
            raise DataNotScrappedError()
        df = pd.read_csv(CACHE_FILE)
        if not filters:
            return list(df.T.to_dict().values())

        filtered_df = df[df['name'] == filters][['category', 'name']]

        return list(filtered_df.T.to_dict().values())

    async def get(self, filters: dict = None):
        """Get data from cached file"""

        res = self.__get_data(filters)

        return res
