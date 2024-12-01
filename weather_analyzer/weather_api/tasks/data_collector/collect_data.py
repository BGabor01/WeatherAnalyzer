import os
import logging
from typing import Dict, Union

from celery import shared_task
from django.utils.dateparse import parse_datetime
from django.db import transaction

from weather_api.models import City, WeatherData
from .wrappers import WeatherStackWrapper
from .rabbit_mq_handler import RabbitMqHandler
from .enums import RoutingKeysEnum, ExchangesEnum


logger = logging.getLogger("data_collector")


def get_city_data(
    data: Dict[str, Union[str, int, float]]
) -> Dict[str, Union[str, int, float]]:
    return {
        "city_id": data["city_id"],
        "name": data["city_name"],
        "country_code": data["country_code"],
        "state_code": data["state_code"],
        "latitude": data["lat"],
        "longitude": data["lon"],
        "timezone": data["timezone"],
        "station_id": data["station_id"],
    }


def create_weather_details(weather, city: City) -> Dict[str, Union[str, int, float]]:
    return {
        "city": city,
        "date": parse_datetime(weather["datetime"]).date(),
        "cloud_cover": weather["clouds"],
        "max_temperature": weather["max_temp"],
        "max_temperature_timestamp": weather["max_temp_ts"],
        "min_temperature": weather["min_temp"],
        "min_temperature_timestamp": weather["min_temp_ts"],
        "max_uv_index": weather["max_uv"],
        "max_wind_direction": weather["max_wind_dir"],
        "max_wind_speed": weather["max_wind_spd"],
        "max_wind_speed_timestamp": weather["max_wind_spd_ts"],
        "avg_wind_speed": weather["wind_spd"],
        "avg_wind_direction": weather["wind_dir"],
        "avg_relative_humidity": weather["rh"],
        "snow": weather["snow"],
        "snow_depth": weather["snow_depth"] or 0,
    }


@shared_task(
    queue="collector_queue",
    name="collect_weather_data_task",
)
def collect_weather_data_task() -> None:
    logger.info("Collect weather data task started!")
    wrapper = WeatherStackWrapper(api_key=os.environ.get("API_KEY"))
    weather_data = wrapper.get_last_week_weather()

    for weather_data_by_city in weather_data:
        city_data = get_city_data(weather_data_by_city)
        city_id = city_data.pop("city_id")
        city, _ = City.objects.get_or_create(id=int(city_id), defaults=city_data)
        weather_detail_instances = [
            WeatherData(**create_weather_details(weather_details, city))
            for weather_details in weather_data_by_city["data"]
        ]
        logger.info(
            f"WeatherData objects created for city_id: {city_id}, city_name: {city.name}"
        )
        with transaction.atomic():
            WeatherData.objects.bulk_create(weather_detail_instances)

    logger.info("Data collection completed successfully. Notifying processor worker!")

    handler = RabbitMqHandler(queue_name="processor_queue")
    handler.publish(
        "calculate_weekly_statistics_task",
        ExchangesEnum.PROCESSOR_E.value,
        RoutingKeysEnum.PROCESSOR_RK.value,
    )
    handler.close()
