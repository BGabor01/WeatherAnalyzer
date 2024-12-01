from datetime import datetime
from django.core.management.base import BaseCommand
from weather_api.tasks.data_collector.collect_data import collect_weather_data_task


class Command(BaseCommand):
    help = "Fetch weather data for a specified date range. Defaults to the task's default values."

    def handle(self, *args, **options):
        collect_weather_data_task.delay()
