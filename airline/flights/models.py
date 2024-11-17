from django.db import models

# Create your models here.


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"
    

class Flight(models.Model):
    #origin = models.CharField(max_length=64) #<-- before applyling foreign key
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") # if an airport would be deleted, it would also delete the corresponding flight.

    #destination = models.CharField(max_length=64) #<-- before applyling foreign key
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")

    duration = models.IntegerField()

    def __str__(self): # returns a string representation of the object
        return f"{self.id}: {self.origin} to {self.destination}"
    

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers") # every passenger could be associated with many flights, blank=True means allowed to be unassociated w a flight.

    def __str__(self):
        return f"{self.first} {self.last}"