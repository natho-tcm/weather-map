import logging

from apscheduler.triggers.interval import IntervalTrigger

from app import settings
from app.containers.cities import City


def add_scheduler_tasks(scheduler, redis):
    """Add tasks to scheduler for fetching weather."""

    for city in settings.CITIES:
        scheduler.add_job(
            fetch_current_weather_task, IntervalTrigger(seconds=city.frequency), (redis, city)
        )


async def fetch_current_weather_task(redis, city: City):
    """Task for fetching weather for given city."""

    logging.info(f'Fetching current weather for "{city.city_name}"')
    await redis.enqueue_job('fetch_current_weather', city)
