import json
import logging
import os

from dotenv import load_dotenv

from app.containers.cities import City

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Weather Map
WEATHER_MAP_API_KEY = os.getenv('WEATHER_MAP_API_KEY')
WEATHER_MAP_URL = os.getenv('WEATHER_MAP_URL')

CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.json')

try:
    with open(CONFIG_FILE_PATH) as file:
        CITIES = [City.parse_obj(city) for city in json.load(file).get('cities')]
except Exception as ex:
    logging.error(f'Could not load config file: {ex}')
    CITIES = []


# DB
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
