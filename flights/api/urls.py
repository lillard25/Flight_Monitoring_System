from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirportViewSet, AirlineViewSet, FlightViewSet, FlightStatusViewSet,
    DelayedFlightViewSet,
    scrape_airport_data, scrape_airline_data
)

router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'flight-status', FlightStatusViewSet)
router.register(r'delayed-flights', DelayedFlightViewSet, basename='delayed-flight')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/scrape-airports/', scrape_airport_data, name="scrape-airports"),
    path('api/scrape-airlines/', scrape_airline_data, name="scrape-airlines"),
]