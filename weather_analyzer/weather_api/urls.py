from django.contrib import admin
from django.urls import path
from .views import (
    ListCitiesView,
    ListHistoricalDataForCityView,
    ListWeeklyStatisticsView,
)

urlpatterns = [
    path("cities/", ListCitiesView.as_view(), name="list-cities-view"),
    path(
        "historical/",
        ListHistoricalDataForCityView.as_view(),
        name="list-historical-data-for-cities",
    ),
    path(
        "statistics/weekly/",
        ListWeeklyStatisticsView.as_view(),
        name="list-weekly-stats",
    ),
]
