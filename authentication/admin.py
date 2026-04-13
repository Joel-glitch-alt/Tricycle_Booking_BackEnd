from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'role', 'is_verified')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('role', 'is_verified')