from django.contrib import admin
from django.urls import path
from .views import ListCitiesView, ListHistoricalDataForCity

urlpatterns = [
    path("cities/", ListCitiesView.as_view(), name="list-cities-view"),
    path(
        "historical/",
        ListHistoricalDataForCity.as_view(),
        name="list-historical-data-for-cities",
    ),
]
