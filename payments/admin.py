from django.contrib import admin

# Register your models here.
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'user', 'booking', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('reference', 'user__username')