from django.contrib.auth.models import AbstractUser
from django.db import models

# Create at least 3 models.
# Models are like tables and columns in the SQL db.

class User(AbstractUser):
    # check 000#_initial.py to see table columns.
    pass


class Listings(models.Model):

    # The first element in each tuple is the name to apply to the group. The second element is an iterable of 2-tuples, with each 2-tuple containing a value and a human-readable name for an option. 

    # Migrate this to the forms.py file.
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'), 
        ('toys', 'Toys'), 
        ('electronics','Electronics'), 
        ('home', 'Home'),
    ]
    
    # Django automatically adds an 'id' field as the primary key
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    imageURL = models.URLField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, default='0.00')
    current_winner = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    created = models.DateTimeField()
    listingClosed = models.BooleanField()  # listing active vs closed.

    # def __str__(self):
    #     return f"{self.col1}, {self.col2}, {self.col3}"

class Bids(models.Model):
    listingId = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bid_listingId")
    bidAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    #bidUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bidUser = models.CharField(max_length=100) #TODO
    biddingDate = models.DateTimeField()
    # def __str__(self):
    #     return f"{self.col1}, {self.col2}, {self.col3}"    
    
class Comments(models.Model):
    listingId = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment_listingId")
    commentBody = models.CharField(max_length=500)
    commentUser = models.CharField(max_length=100) #TODO
    commentDate = models.DateTimeField()
    # def __str__(self):
    #     return f"{self.col1}, {self.col2}, {self.col3}"


class Watchlist(models.Model):
    listingId = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist_listingId")
    watchlistUser = models.CharField(max_length=100) #TODO
    # def __str__(self):
    #     return f"{self.col1}, {self.col2}, {self.col3}"