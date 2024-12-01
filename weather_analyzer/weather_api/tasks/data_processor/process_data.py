import time
import logging
from datetime import datetime, timedelta, date
from typing import Dict, Tuple

from django.db import connections
from django.db.models import Avg, Sum, F
from django.db import transaction
from celery import shared_task

from weather_api.models import WeatherData, WeeklyWeatherStatistics


logger = logging.getLogger("data_processor")


def get_week_dates() -> Tuple[date, date]:
    today = datetime.now().date()
    week_start_date = today - timedelta(days=7)

    return week_start_date, today


def wait_for_replica_sync(timeout=5, poll_interval=0.1):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            with connections["default"].cursor() as primary_cursor, connections[
                "replica"
            ].cursor() as replica_cursor:
                primary_cursor.execute("SELECT pg_current_wal_lsn();")
                primary_lsn = primary_cursor.fetchone()[0]

                replica_cursor.execute("SELECT pg_last_wal_replay_lsn();")
                replica_lsn = replica_cursor.fetchone()[0]

                if primary_lsn == replica_lsn:
                    logger.info(
                        "Replica is fully synchronized with the primary database."
                    )
                    return
                else:
                    logger.warning(
                        f"Replica is out of sync with the primary database. Sync mismatch detected. Wait {poll_interval} seconds."
                    )

        except Exception as e:
            raise RuntimeError(f"Error while checking replica sync: {e}")

        time.sleep(poll_interval)

    raise TimeoutError(f"Replica did not sync within {timeout} seconds.")


def create_weekly_statistics(
    city_id: int, week_start_date: datetime, data: Dict[str, float]
) -> WeeklyWeatherStatistics:
    return WeeklyWeatherStatistics(
        city_id=city_id,
        week_start_date=week_start_date,
        avg_temperature=data["avg_temperature"],
        avg_wind_speed=data["avg_wind_speed"],
        total_snowfall=data["total_snowfall"],
        avg_cloud_cover=data["avg_cloud_cover"],
        avg_uv_index=data["avg_uv_index"],
        avg_week_relative_humidity=data["avg_week_relative_humidity"],
    )


@shared_task(queue="processor_queue", name="calculate_weekly_statistics_for_city")
def calculate_weekly_statistics_for_city(
    city_id: int, week_start_date: datetime, data: Dict[str, float]
) -> None:
    try:
        weekly_stat = create_weekly_statistics(city_id, week_start_date, data)
        with transaction.atomic(using="default"):
            WeeklyWeatherStatistics.objects.bulk_create([weekly_stat])

        logger.info(f"Weekly statistics created for city {city_id}.")

    except Exception as e:
        logger.error(f"Error processing city {city_id}: {e}")
        raise


@shared_task(queue="processor_queue", name="calculate_weekly_statistics_task")
def calculate_weekly_statistics_task() -> None:
    wait_for_replica_sync()
    week_start_date, today = get_week_dates()

    aggregated_data = (
        WeatherData.objects.filter(date__gte=week_start_date, date__lte=today)
        .values("city_id")
        .annotate(
            avg_temperature=Avg((F("max_temperature") + F("min_temperature")) / 2.0),
            avg_wind_speed=Avg("avg_wind_speed"),
            total_snowfall=Sum("snow"),
            avg_cloud_cover=Avg("cloud_cover"),
            avg_uv_index=Avg("max_uv_index"),
            avg_week_relative_humidity=Avg("avg_relative_humidity"),
        )
    )

    for data in aggregated_data:
        city_id = data["city_id"]
        calculate_weekly_statistics_for_city.apply_async(
            (city_id, week_start_date, data)
        )

    logger.info("All weekly statistics calculations have been queued.")
