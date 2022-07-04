import logging
from decimal import Decimal
from typing import Dict

from aiohttp import ClientSession
from arq.connections import RedisSettings

from app import settings
from app.containers.cities import City
from app.db.services import db_service


def log_for_diff(content: Dict, last_weather_record: Dict, city: City):
    if last_weather_record:
        diff = Decimal(
            abs(
                100 - (Decimal(content['main']['temp']) / Decimal(last_weather_record['temperature']) * 100)
            ).quantize(Decimal('0'))
        )

        if diff == city.threshold:
            logging.warning(f'Temperature for city "{city.city_name}" has been changed!')


async def fetch_current_weather(ctx, city: City):
    """Fetch current weather for given city."""

    params = {'appid': settings.WEATHER_MAP_API_KEY, 'q': city.city_name, 'units': 'metric'}
    session: ClientSession = ctx['session']

    async with session.get(url=settings.WEATHER_MAP_URL, params=params) as response:
        if response.status != 200:
            response.raise_for_status()

        content = await response.json()

        last_weather_record = await db_service.fetch_the_last_weather_record_by_city(city_name=city.city_name)

        log_for_diff(content, last_weather_record, city)
        await save_weather_record(content=content)


async def save_weather_record(content: dict):
    """Save current weather to DB."""

    await db_service.insert_weather_record(
        city_name=content['name'],
        temperature=content['main']['temp'],
        wind_speed=content['wind']['speed'],
    )


async def startup(ctx):
    """Worker startup function."""

    ctx['session'] = ClientSession()


async def shutdown(ctx):
    """Worker shutdown function."""

    await ctx['session'].close()


class WorkerSettings:
    """ARQ worker settings."""

    functions = [fetch_current_weather]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
