from django.contrib import admin


from .models import Flight, Airport, Passenger
# Register your models here.

# How to configure the Flight section on the admin it to show additional customized information.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

# How to apply a horizontal filter to the Passenger section of the Admin page
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # apply FlightAdmin created above.
admin.site.register(Passenger, PassengerAdmin) # apply PassengerAdmin created above.