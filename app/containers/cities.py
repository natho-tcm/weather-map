from pydantic import BaseModel


class City(BaseModel):
    city_id: int
    city_name: str
    frequency: int
    threshold: int
