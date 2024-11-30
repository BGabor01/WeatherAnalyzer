from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from .models import City, WeatherData
from .serializers import CitySerializer, HistoricalDataSerializer
from .filters import CityFilter, HistoricalDataFilter


class ListCitiesView(ListAPIView):
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CityFilter
    queryset = City.objects.all()


class ListHistoricalDataForCity(ListAPIView):
    serializer_class = HistoricalDataSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HistoricalDataFilter
    queryset = WeatherData.objects.all()
