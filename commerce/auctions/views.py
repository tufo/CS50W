from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listings, Bids, Comments

from datetime import datetime


def index(request):
    # render index.html and send all the entries from the Listings class.
    return render(request, "auctions/index.html", {
    "listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):

    if request.method == "POST":

        # grab the values from the form and populate them into variables.
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        imageURL = request.POST["imageURL"]
        category = request.POST["category"]
        current_price = startingBid # change this later

        # create an entry (row) in the table Listings.
        listing = Listings(
            title=title, 
            description=description, 
            starting_bid=startingBid,
            imageURL=imageURL,
            category=category,
            current_price=current_price,
            created=datetime.now(),
            listingClosed=False
            )
        
        # Save it to the db.
        listing.save()

        # pk id was created automatically.
        # pass the listing id to the page so that after submission, listing.html can access it.
        return redirect(reverse('listing', args=(listing.id, )))

    
    # if accessing the page via "GET"
    return render(request, "auctions/create.html")


def listing(request, listing_id): # extract the listing id from the URL.
    
    # if accessing listing.html through GET:

    listing = Listings.objects.get(id=listing_id)

    # pass variables to the listing page for it to populate the HTML.
    return render(request, "auctions/listing.html", {
        "listing": listing,
    })


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def categories(request):
    return render(request, "auctions/categories.html")

def bid(request):
    return render(request, "auctions.html")