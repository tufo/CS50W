from django.contrib.auth.models import AbstractUser
from django.db import models

# Create at least 3 models.
# Models are like tables and columns in the SQL db.

class User(AbstractUser):
    # check 000#_initial.py to see table columns.
    pass

class Listings(models.Model):

    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'), 
        ('toys', 'Toys'), 
        ('electronics','Electronics'), 
        ('home', 'Home'),
    ]
    
    # Django automatically adds an 'id' field as the primary key
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    imageURL = models.URLField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField()
    listingClosed = models.BooleanField()  # listing active vs closed.

    # def __str__(self):
    #     return f"{self.col1}, {self.col2}, {self.col3}"
    
class Bids(models.Model):
    #TODO
    def __str__(self):
        return f"{self.col1}, {self.col2}, {self.col3}"
    
class Comments(models.Model):
    #TODO
    def __str__(self):
        return f"{self.col1}, {self.col2}, {self.col3}"