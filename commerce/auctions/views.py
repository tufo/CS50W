from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments, Watchlist
from .forms import ListingForm

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

@login_required
def create(request):

    user = request.user.username

    if request.method == "POST":

        # grab the values from the form and populate them into variables.
        title = request.POST["title"]
        description = request.POST["description"]
        imageURL = request.POST["imageURL"]
        category = request.POST["category"]
        createdDateTime=datetime.now()
        startingBid = request.POST["startingBid"]
        user = request.user.username


        # create an entry (row) in the table Listings.
        listing = Listings(
            title=title, 
            description=description, 
            imageURL=imageURL,
            category=category,
            starting_bid=startingBid,            
            current_price=startingBid,
            creator=user,
            created=createdDateTime,
            listingClosed=False
            )
        
        # Save it to the db.
        listing.save()

        # create an entry in Bids table.
        bid = Bids(
            listingId=listing,  # pk id was created automatically; notice that i have to use 'listing', and not 'listing.id'
            bidAmt=startingBid,
            bidUser=user,
            biddingDate=createdDateTime
        )

        bid.save()

        # pk id was created automatically.
        # pass the listing id to the page so that after submission, listing.html can access it.
        return redirect(reverse('listing', args=(listing.id, )))

    
    # if accessing the page via "GET"
    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })

@login_required
def listing(request, listing_id): # extract the listing id from the URL.
    
    # query the listing information
    listing = Listings.objects.get(pk=listing_id) # listing_id obtained from the URL input.

    user = request.user.username

    # SUBFUNCTION: FORM SUBMIT PLACING BID.
    # if accessing listing.html through POST:
    if request.method == "POST" and 'placeBid' in request.POST:

        # grab the bid value submitted.
        bidAmt = request.POST["placeBid"]

        # create an entry in Bids table.
        bid = Bids(
            listingId=listing,
            bidAmt=bidAmt,
            bidUser=user,
            biddingDate=datetime.now()
        )

        # write the bid amount to the Bids table.
        bid.save()

        # update the current_price of the listing via a query.
        listing.current_price=bidAmt # pay attention to the syntax for how to update the current_price field.
        listing.current_winner=user
        listing.save()
    
    # SUBFUNCTION: FORM SUBMIT ADDING TO WATCHLIST.
    # if statement when adding to WATCHLIST.
    elif request.method == "POST" and 'addToWatchlist' in request.POST:
    
        # check if listing is already in watchlist.
        watchlistXCheck = Watchlist.objects.filter(listingId=listing_id, watchlistUser=user)

        if len(watchlistXCheck) > 0: # > 0 means it already exists.
            print("This entry already exists in your watchlist.")
       
        else: # if the listing isn't in the watchlist already, create an entry and write to Watchlist table.
            watchlistEntry = Watchlist(
                listingId=listing,
                watchlistUser=user
            )
            watchlistEntry.save()

    # SUBFUNCTION: FORM POST TO CLOSE THE AUCTION LISTING.
    elif request.method == "POST" and 'close_listing' in request.POST:
        if user == listing.creator:
            listing.listingClosed = True
            listing.save()
        else:
            print("You are not authorized to deactivate this listing.")

    # SUBFUNCITON: FORM POST TO (RE)OPEN AUCTION LISTING
    elif request.method == "POST" and 'open_listing' in request.POST:
        if user == listing.creator:
            listing.listingClosed = False
            listing.save()
        else:
            print("You are not authorized to activate this listing.")


    # SUBFUNCTION: FORM SUBMIT ADDING COMMENT.
    elif request.method == "POST" and 'submitComment' in request.POST:
        comment_body = request.POST["submitComment"]
        commentEntry = Comments(
            listingId=listing,
            commentBody=comment_body,
            commentUser=user,
            commentDate=datetime.now()
        )
        commentEntry.save()

    # Query and display the bidding history for this listing
    #bidHistory = Bids.objects.get(listingId=listing)
    bidHistory = Bids.objects.filter(listingId=listing)

    # Query and display the comments history for this listing
    commentHistory = Comments.objects.filter(listingId=listing)

    # ATTEMPTING TO USE forms.Form
    # form = ListingForm()


    # pass variables to the listing page for it to populate the HTML.
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_history":bidHistory,
        "comment_history":commentHistory
        # 'form': form
    })

@login_required
def watchlist(request):

    # grab the user.
    user = request.user.username

    # query the user's watchlist entries from the db.
    watchlist = Watchlist.objects.filter(watchlistUser=user)
    #watchlist = Watchlist.objects.all()

    if request.method == "POST":
        
        # get submission from post
        listing = request.POST["watchlistEntry"]
        watchlistEntry = Watchlist.objects.filter(listingId=listing, watchlistUser=user)
        watchlistEntry.delete()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

# see urls.py for how to define paths for optional URL parameters.
def categories(request, Category=None):
# def categories(request):

    # if a category has been submitted.
    if Category:
        
        # override Category.
        # Category = 'home'

        # query listings and filter where category is the selected category.
        listings_in_category = Listings.objects.filter(category=Category)

        return render(request, "auctions/categories.html", {
            "listingsInCategory": listings_in_category
        })

    # create a form object
    form = ListingForm()

    # extract the list of choices from it.
    category_choices = form.CATEGORY_CHOICES

    # create an empty list.
    catChoiceList = []
    # convert from a list of tuples into a simple list.
    for n in range(int(len(category_choices))):
        # populate the list.
        catChoiceList.append(category_choices[n][0])

    return render(request, "auctions/categories.html", {
        "categories": catChoiceList
    })