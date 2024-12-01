from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from .models import City, WeatherData, WeeklyWeatherStatistics
from .serializers import (
    CitySerializer,
    HistoricalDataSerializer,
    WeeklyStatisticsSerializer,
)
from .filters import CityFilter, HistoricalDataFilter, WeeklyStatisticsFilter


class ListCitiesView(ListAPIView):
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CityFilter
    queryset = City.objects.all()


class ListHistoricalDataForCityView(ListAPIView):
    serializer_class = HistoricalDataSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HistoricalDataFilter
    queryset = WeatherData.objects.all()


class ListWeeklyStatisticsView(ListAPIView):
    serializer_class = WeeklyStatisticsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WeeklyStatisticsFilter
    queryset = WeeklyWeatherStatistics.objects.all()
