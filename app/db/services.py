import datetime
from typing import List, Optional

from app.db.client import PostgresClient


class DatabaseService:
    """Database service class."""

    def __init__(self):
        self.client = PostgresClient()

    async def fetch_the_last_weather_records(self) -> List[dict]:
        """Return the last weather records for each city."""

        command = 'SELECT DISTINCT ON (city_name) * FROM weathers ORDER BY city_name, created_at DESC;'
        result = await self.client.execute(command, fetch=True)

        return [dict(row.items()) for row in result]

    async def fetch_the_last_weather_record_by_city(self, city_name: str) -> Optional[dict]:
        """Return the last weather record for given city."""

        command = 'SELECT * FROM weathers WHERE city_name = $1 ORDER BY created_at DESC'
        result = await self.client.execute(command, city_name, fetchrow=True)

        return dict(result.items()) if result else None

    async def insert_weather_record(self, city_name: str, temperature: float, wind_speed: float):
        """Insert weather record into DB."""

        command = 'INSERT INTO weathers(city_name, temperature, wind_speed, created_at) VALUES($1, $2, $3, $4)'
        args = city_name, temperature, wind_speed, datetime.datetime.now()
        result = await self.client.execute(command, *args, execute=True)

        return result


db_service = DatabaseService()
