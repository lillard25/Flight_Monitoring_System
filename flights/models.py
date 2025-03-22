from django.db import models

class Airport(models.Model):
    name = models.CharField(max_length=255, null=True)
    iata_code = models.CharField(max_length=10, null=True)
    icao_code = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name} ({self.icao_code})"


class Airline(models.Model):
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=10)
    icao_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.flight_number} ({self.departure_airport} → {self.arrival_airport})"


class FlightStatus(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('on-time', 'On Time'), ('delayed', 'Delayed'), ('cancelled', 'Cancelled')])
    delay_minutes = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


class DelayedFlight(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    delay_reason = models.TextField()
    delay_duration = models.IntegerField()
    reported_at = models.DateTimeField(auto_now_add=True)


class FlightPrice(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flight.flight_number} - {self.price} {self.currency}"


class LogEntry(models.Model):
    event_type = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
