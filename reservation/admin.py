from django.contrib import admin

from .models import House, ListingOwner, Reservation, Room

admin.site.register(ListingOwner)
admin.site.register(House)
admin.site.register(Room)
admin.site.register(Reservation)



