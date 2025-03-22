from rest_framework import serializers
from flights.models import Airport, Airline, Flight, FlightStatus, DelayedFlight, FlightPrice, LogEntry

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    departure_airport = AirportSerializer(read_only=True)
    arrival_airport = AirportSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

class AirportHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['name']

class AirlineHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['name']


class FlightStatusHelperSerializer(serializers.ModelSerializer):
    departure_airport = AirportHelperSerializer(read_only=True)
    arrival_airport = AirportHelperSerializer(read_only=True)
    airline = AirlineHelperSerializer(read_only=True)

    class Meta:
            model = Flight
            fields = ['flight_number', 'departure_airport', 'arrival_airport', 'airline']

class FlightStatusSerializer(serializers.ModelSerializer):
    flight = FlightStatusHelperSerializer(read_only=True)

    class Meta:
        model = FlightStatus
        fields = ['id', 'flight', 'status', 'delay_minutes']

class DelayedFlightSerializer(serializers.ModelSerializer):
    flight = FlightStatusHelperSerializer(read_only=True)

    class Meta:
        model = FlightStatus
        fields = ['id', 'flight', 'delay_minutes']
