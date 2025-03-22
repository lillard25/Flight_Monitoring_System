from rest_framework import viewsets
from flights.models import Airport, Airline, Flight, FlightStatus, DelayedFlight, FlightPrice, LogEntry
from .serializers import (
    AirportSerializer, AirlineSerializer, FlightSerializer,
    FlightStatusSerializer, DelayedFlightSerializer
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from flights.scraping.scrape_airports import scrape_airports
from flights.scraping.scrape_airlines import scrape_airlines


@api_view(["POST"])
def scrape_airport_data(request):
    """Trigger the airport data scraping process."""
    scrape_airports()
    return Response({"message": "Airport data scraped successfully!"})


@api_view(["POST"])
def scrape_airline_data(request):
    """Trigger the airline data scraping process."""
    scrape_airlines()
    return Response({"message": "Airline data scraped successfully!"})

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightStatusViewSet(viewsets.ModelViewSet):
    queryset = FlightStatus.objects.all()
    serializer_class = FlightStatusSerializer

class DelayedFlightViewSet(viewsets.ModelViewSet):
    serializer_class = DelayedFlightSerializer

    def get_queryset(self):
        # Filter FlightStatus entries with delay_minutes > 120
        return FlightStatus.objects.filter(delay_minutes__gt=120)



