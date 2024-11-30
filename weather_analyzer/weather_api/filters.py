from django_filters import rest_framework as filters
from .models import City, WeatherData


class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = ("id", "name", "country_code")


class HistoricalDataFilter(filters.FilterSet):
    class Meta:
        model = WeatherData
        fields = ("city__id", "city__name", "date")
