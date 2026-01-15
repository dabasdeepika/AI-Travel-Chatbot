from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Flight
from .serializers import HotelSerializer, FlightSerializer

class HotelSuggestionAPI(APIView):
    def get(self, request):
        city = request.GET.get("city")
        category = request.GET.get("category")
        hotels = Hotel.objects.filter(city__iexact=city, category__iexact=category)[:4]
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

class FlightSuggestionAPI(APIView):
    def get(self, request):
        departure = request.GET.get("departure")
        arrival = request.GET.get("arrival")
        category = request.GET.get("category")
        flights = Flight.objects.filter(departure__iexact=departure, arrival__iexact=arrival, category__iexact=category)[:3]
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
