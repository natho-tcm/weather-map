from orjson import dumps
from sanic import Sanic

from app.web.api.v1.blueprints import api_v1


def create_app() -> Sanic:
    app = Sanic("weather-server", dumps=dumps)
    app.blueprint(api_v1)

    settings = {}
    app.config.update_config(settings)

    return app
