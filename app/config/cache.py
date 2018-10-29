import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CACHE_FILE_NAME = 'games.csv'

CACHE_FILE = os.path.join(BASE_DIR, 'storage', CACHE_FILE_NAME)
