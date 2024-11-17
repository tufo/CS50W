from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
    "flights": Flight.objects.all() # give index.html access to this variable.
    })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    #flight = Flight.objects.get(pk=flight_id) # can also use pk for primary key
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(), # give it access to the passengers on that flight. these are the people who are on the flight.
        "non_passengers": Passenger.objects.exclude(flights=flight).all() # this excludes people who are already on the flight. this allows for the HTML dropdown.
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"])) 
        # request.POST["passenger"]... the data about which passenger id we want in this advice will be in a form where the input field is named "passenger"
        # next, i want to get the flight id
        # they should tell me what the id is of the passenger.
        # the data about which passenger ID we want to register we want, will be passed in by a form.
        passenger.flights.add(flight) # this will add a new row into the table.
        
        # what URL would i like to take them to? the flight route.
        # takes the name of a particular view and gives us what the URL is.
        # the flight route takes an arguement, written as a tuple.
        # make sure the right imports are imported.
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
