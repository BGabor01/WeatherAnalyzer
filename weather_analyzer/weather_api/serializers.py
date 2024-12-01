from rest_framework import serializers
from .models import City, WeatherData, WeeklyWeatherStatistics


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class HistoricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = "__all__"


class WeeklyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyWeatherStatistics
        fields = "__all__"
