from django.contrib import admin

from .models import Watchlist, Comments, Bids, Listings, User

# Register your models here.
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Listings)
admin.site.register(User)
