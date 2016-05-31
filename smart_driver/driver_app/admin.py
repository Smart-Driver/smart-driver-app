from django.contrib import admin
from .models import Ride, WeekStatement, Driver, DayStatement

admin.site.register(Ride)
admin.site.register(WeekStatement)
admin.site.register(Driver)
admin.site.register(DayStatement)
