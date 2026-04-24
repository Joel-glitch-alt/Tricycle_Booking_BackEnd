from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'driver', 'passengers', 'pickup_location', 'destination', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'driver__full_name', 'destination')  # ← can search by destination too
    fields = ('user', 'driver', 'passengers', 'pickup_location', 'destination', 'status')  # ← makes them editable in the form