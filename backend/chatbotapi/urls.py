from django.urls import path
from .views import HotelSuggestionAPI, FlightSuggestionAPI

urlpatterns = [
    path('hotels/', HotelSuggestionAPI.as_view(), name='hotel-suggestions'),
    path('flights/', FlightSuggestionAPI.as_view(), name='flight-suggestions'),
]
