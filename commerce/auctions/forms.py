from django import forms
from .models import Listings


# Instructions in Lecture Django @ 1:19:00 of video.
class ListingForm(forms.Form):
    
    # the following code displays a dropdown of listing IDs in the form.
    # get rid of this code if you don't want that.
    #listing = forms.ModelChoiceField(queryset=Listings.objects.all())

    # dropdown, choices, choicefield.
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'), 
        ('toys', 'Toys & Games'), 
        ('electronics','Electronics'), 
        ('home', 'Home'),
        ('appliances', 'Apppliances'),
        ('office supplies', 'Office Supplies'),
        ('automotive', 'Automotive'),
        ('health', 'Self Care'),
        ('furniture', 'Furniture'),
        ('equipment', 'Equipment'),
        ('jewelry', 'Jewelry'),
        ('instruments', 'Musical Instruments'),
        ('sporting', 'Sporting'),
        ('tickets', 'Tickets'),
        ('tools', 'Tools'),
        ('multimedia', 'Multimedia')
    ]

    # define all of the fields (inputs) for the user to provide

    title = forms.CharField(label="Title")
    # the left startingBid is the html name for the input field.
    # make sure it matches with the def function in views.py that is receiving the value.
    startingBid = forms.DecimalField(label="Starting Bid")
    description = forms.CharField(label="Description")
    imageURL = forms.URLField(label="Image URL")
    category = forms.ChoiceField(label="Category", choices = CATEGORY_CHOICES)

