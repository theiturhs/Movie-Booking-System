from django.contrib import admin
from .models import *

admin.site.register(City)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(SeatStatus)