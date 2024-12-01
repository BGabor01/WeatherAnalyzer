from django_filters import rest_framework as filters
from .models import City, WeatherData, WeeklyWeatherStatistics


class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = ("id", "name", "country_code")


class HistoricalDataFilter(filters.FilterSet):
    class Meta:
        model = WeatherData
        fields = ("city__id", "city__name", "date")


class WeeklyStatisticsFilter(filters.FilterSet):
    class Meta:
        model = WeeklyWeatherStatistics
        fields = ("city__id", "city__name", "week_start_date")
