from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    # These are the columns you will see in the list
    list_display = ('full_name', 'vehicle', 'rating', 'is_available')
    # This adds the search bar
    search_fields = ('full_name', 'vehicle')
    # This adds the filter sidebar
    list_filter = ('is_available',)