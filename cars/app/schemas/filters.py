from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from cars.app.models import Car as CarModel


class CarFilter(Filter):
    brand__in: Optional[list[str]] = Field(default=None)

    year__gte: Optional[int] = Field(default=None)
    year__lte: Optional[int] = Field(default=None)

    engine_type__eq: Optional[str] = Field(default=None)

    fuel_type__in: Optional[list[str]] = Field(default=None)

    class Constants(Filter.Constants):
        model = CarModel
