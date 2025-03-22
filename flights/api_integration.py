import requests
from django.utils.timezone import now, make_aware
from datetime import datetime
from .models import Flight, FlightStatus, DelayedFlight, Airline, Airport, LogEntry

# API Configuration
AVIATIONSTACK_API_KEY = "YOUR_API_KEY"
FLIGHTS_URL = "http://api.aviationstack.com/v1/flights"


def fetch_flight_data():
    """Fetch flight data from AviationStack API and update the database."""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "limit": 100,
        "flight_region": "EU",
    }

    try:
        response = requests.get(FLIGHTS_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        LogEntry.objects.create(
            event_type="API_ERROR",
            description=f"Failed to fetch flight data: {str(e)}"
        )
        return

    if response.status_code == 200:
        data = response.json().get("data", [])

        for flight_data in data:
            try:
                flight_number = flight_data.get("flight", {}).get("iata", "")
                airline_name = flight_data.get("airline", {}).get("name", "")
                departure_code = flight_data.get("departure", {}).get("iata", "")
                arrival_code = flight_data.get("arrival", {}).get("iata", "")
                departure_time_str = flight_data.get("departure", {}).get("estimated", None)
                arrival_time_str = flight_data.get("arrival", {}).get("estimated", None)
                status = flight_data.get("flight_status", "unknown")
                delay_minutes = flight_data.get("arrival", {}).get("delay", 0) or 0

                # Skip if required fields are missing
                if not (flight_number and departure_code and arrival_code):
                    continue

                # Parse datetime strings into timezone-aware datetime objects
                departure_time = (
                    make_aware(datetime.fromisoformat(departure_time_str))
                    if departure_time_str else None
                )
                arrival_time = (
                    make_aware(datetime.fromisoformat(arrival_time_str))
                    if arrival_time_str else None
                )

                # Get or create Airline
                airline, _ = Airline.objects.get_or_create(name=airline_name)

                # Get departure and arrival airports
                departure_airport = Airport.objects.filter(iata_code=departure_code).first()
                arrival_airport = Airport.objects.filter(iata_code=arrival_code).first()

                if departure_airport and arrival_airport:
                    # Update or create Flight
                    flight, created = Flight.objects.update_or_create(
                        flight_number=flight_number,
                        defaults={
                            "airline": airline,
                            "departure_airport": departure_airport,
                            "arrival_airport": arrival_airport,
                            "departure_time": departure_time,
                            "arrival_time": arrival_time,
                        }
                    )

                    # Update Flight Status
                    FlightStatus.objects.update_or_create(
                        flight=flight,
                        defaults={"status": status}
                    )

                    # Log delayed flights (delay > 2 hours)
                    if delay_minutes and delay_minutes > 120:
                        DelayedFlight.objects.create(
                            flight=flight,
                            delay_reason="Operational Issue",
                            delay_duration=delay_minutes
                        )

                    # Log the update
                    LogEntry.objects.create(
                        event_type="FLIGHT_UPDATE",
                        description=f"Updated flight {flight_number}."
                    )

            except Exception as e:
                LogEntry.objects.create(
                    event_type="PROCESSING_ERROR",
                    description=f"Error processing flight {flight_number}: {str(e)}"
                )