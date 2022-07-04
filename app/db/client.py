import asyncpg

from app import settings


class PostgresClient:
    """Postgres client class."""

    @staticmethod
    async def create_pool():
        """Return created asyncpg pool"""

        return await asyncpg.create_pool(
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

    async def _dispatch_method(
            self,
            connection,
            command: str,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        """General dispatcher for connection execution"""
        if fetch:
            return await connection.fetch(command, *args)
        elif fetchval:
            return await connection.fetchval(command, *args)
        elif fetchrow:
            return await connection.fetchrow(command, *args)
        elif execute:
            return await connection.execute(command, *args)

    async def execute(
            self,
            command: str,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        """General method for executing SQL commands."""

        result = None
        pool = await self.create_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
               result = await self._dispatch_method(
                   connection,
                   command,
                   *args,
                   fetch=fetch,
                   fetchval=fetchval,
                   fetchrow=fetchrow,
                   execute=execute,
               )
        await pool.close()

        return result

    async def check_table_exists(self) -> bool:
        """Check weather table existence."""

        command = """
        SELECT EXISTS(SELECT * FROM information_schema.tables where lower(table_name) = lower($1));
        """
        result = await self.execute(command, 'weathers', fetchval=True)

        return result

    async def create_weather_table(self):
        """Create weather table."""

        pool = await self.create_pool()
        command = """
            CREATE TABLE weathers(
                id serial PRIMARY KEY,
                city_name text,
                temperature float,
                wind_speed float,
                created_at timestamp
            )
        """
        async with pool.acquire() as conn:
            await conn.execute(command)
        await pool.close()
