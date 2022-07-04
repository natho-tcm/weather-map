from apscheduler.schedulers.asyncio import AsyncIOScheduler
from arq import create_pool
from arq.connections import RedisSettings

from app import settings
from app.web.app import create_app
from app.db.services import db_service
from app.scheduler.tasks import add_scheduler_tasks

app = create_app()
scheduler = AsyncIOScheduler()


@app.listener("before_server_start")
async def before_server_start(app, loop):
    """Function that runs before server start."""

    if not await db_service.client.check_table_exists():
        await db_service.client.create_weather_table()

    redis = await create_pool(RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT))
    add_scheduler_tasks(scheduler=scheduler, redis=redis)
    scheduler.start()


@app.listener("after_server_stop")
async def after_server_stop(app, loop):
    """Function that runs after server stop."""

    scheduler.shutdown()
