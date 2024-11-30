from django.db import models


class City(models.Model):
    city_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, db_index=True)
    country_code = models.CharField(max_length=2, db_index=True)
    state_code = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone = models.CharField(max_length=255)
    station_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WeatherData(models.Model):
    city = models.ForeignKey(
        City, related_name="weather_data", on_delete=models.CASCADE
    )
    date = models.DateField(db_index=True)
    cloud_cover = models.IntegerField()
    max_temperature = models.FloatField()
    max_temperature_timestamp = models.BigIntegerField()
    min_temperature = models.FloatField()
    min_temperature_timestamp = models.BigIntegerField()
    max_uv_index = models.FloatField()
    max_wind_direction = models.FloatField()
    max_wind_speed = models.FloatField()
    max_wind_speed_timestamp = models.BigIntegerField()
    avg_wind_speed = models.FloatField()
    avg_wind_direction = models.FloatField()
    avg_relative_humidity = models.IntegerField()
    snow = models.FloatField()
    snow_depth = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["city", "date"]),
        ]

    def __str__(self):
        return f"Weather data for {self.city.name} on {self.date}"


class WeeklyWeatherStatistics(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="weekly_statistics"
    )
    week_start_date = models.DateField(db_index=True)
    avg_temperature = models.FloatField()
    avg_max_wind_speed = models.FloatField()
    avg_precipitation = models.FloatField()
    total_snowfall = models.FloatField()
    avg_cloud_cover = models.FloatField()
    avg_uv_index = models.FloatField()
    avg_min_relative_humidity = models.FloatField()
    avg_max_relative_humidity = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["city", "week_start_date"]),
        ]

    def __str__(self):
        return f"Weekly statistics for {self.city.name} starting {self.week_start_date}"
