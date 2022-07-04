from sanic import Blueprint, json

from app.db.services import db_service

api_v1 = Blueprint(name="v1_blueprint", url_prefix='/api/v1')


@api_v1.get("/weather")
async def get_weathers(request):
    result = await db_service.fetch_the_last_weather_records()

    return json(result)
