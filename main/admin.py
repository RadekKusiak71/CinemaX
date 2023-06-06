from django.contrib import admin
from .models import UserProfile, Movie, Room,Seat,Ticket

admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Room)
admin.site.register(Seat)
admin.site.register(Ticket)